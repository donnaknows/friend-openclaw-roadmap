#!/usr/bin/env python3
"""notion-cli: Lightweight CLI for Notion API operations.

Usage:
  notion-cli discover [--include-inline]
  notion-cli search <query> [--type page|data_source] [--limit N]
  notion-cli get-page <page_id>
  notion-cli get-db <database_id>
  notion-cli get-ds <data_source_id>
  notion-cli query <data_source_id> [--filter JSON] [--sort JSON] [--limit N] [--props PROP1,PROP2]
  notion-cli create-page <data_source_id> --props JSON [--props-file PATH] [--template default] [--wait-for-template SECS]
  notion-cli update-page <page_id> --props JSON [--props-file PATH]
  notion-cli archive-page <page_id>
  notion-cli get-blocks <block_id> [--limit N]
  notion-cli append-blocks <page_id> --blocks JSON

Environment:
  NOTION_API_TOKEN  - Notion integration token (required)

All output is JSON for easy parsing by agents.
"""

import argparse
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests library not installed. Run: pip install requests"}))
    sys.exit(1)

BASE_URL = "https://api.notion.com/v1"
API_VERSION = "2025-09-03"


def get_token():
    token = os.environ.get("NOTION_API_TOKEN")
    if not token:
        print(json.dumps({"error": "NOTION_API_TOKEN not set"}))
        sys.exit(1)
    return token


def headers():
    return {
        "Authorization": f"Bearer {get_token()}",
        "Notion-Version": API_VERSION,
        "Content-Type": "application/json",
    }


def api_request(method, path, body=None, params=None, max_retries=3):
    url = f"{BASE_URL}{path}"
    for attempt in range(max_retries):
        if method == "GET":
            resp = requests.get(url, headers=headers(), params=params, timeout=30)
        elif method == "POST":
            resp = requests.post(url, headers=headers(), json=body, params=params, timeout=30)
        elif method == "PATCH":
            resp = requests.patch(url, headers=headers(), json=body, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 2))
            if attempt < max_retries - 1:
                time.sleep(retry_after)
                continue
        break

    try:
        data = resp.json()
    except Exception:
        data = {"status_code": resp.status_code, "text": resp.text}

    if resp.status_code >= 400:
        return {"error": True, "status": resp.status_code, "body": data}
    return data


def paginate_all(method, path, body=None, params=None, limit=None):
    results = []
    cursor = None
    while True:
        req_body = dict(body or {})
        if cursor:
            req_body["start_cursor"] = cursor
        req_body["page_size"] = min(limit - len(results), 100) if limit else 100

        data = api_request(method, path, body=req_body, params=params)
        if "error" in data:
            return data

        results.extend(data.get("results", []))
        if not data.get("has_more") or (limit and len(results) >= limit):
            break
        cursor = data.get("next_cursor")

    return {"results": results, "total": len(results)}


def extract_data_source_summary(obj):
    title_parts = obj.get("title", [])
    title = "".join(t.get("plain_text", "") for t in title_parts) or "(untitled)"
    props = {}
    for name, prop in obj.get("properties", {}).items():
        ptype = prop.get("type", "unknown")
        info = {"type": ptype}
        if ptype == "select":
            info["options"] = [o["name"] for o in prop.get("select", {}).get("options", [])]
        elif ptype == "multi_select":
            info["options"] = [o["name"] for o in prop.get("multi_select", {}).get("options", [])]
        elif ptype == "status":
            info["options"] = [o["name"] for o in prop.get("status", {}).get("options", [])]
        props[name] = info
    return {
        "id": obj.get("id", ""),
        "title": title,
        "url": obj.get("url", ""),
        "parent": obj.get("parent", {}),
        "is_inline": obj.get("is_inline", False),
        "properties": props,
    }


def cmd_discover(args):
    data = paginate_all(
        "POST",
        "/search",
        body={"filter": {"property": "object", "value": "data_source"}},
        limit=50,
    )
    if "error" in data:
        return data

    items = []
    for obj in data.get("results", []):
        if obj.get("is_inline", False) and not args.include_inline:
            continue
        if obj.get("in_trash", False):
            continue
        items.append(extract_data_source_summary(obj))

    items.sort(key=lambda d: (d.get("is_inline", False), d.get("title", "")))
    return {"databases": items, "total": len(items)}


def cmd_search(args):
    body = {}
    if args.query:
        body["query"] = args.query
    if args.type:
        body["filter"] = {"property": "object", "value": args.type}
    body["sort"] = {"timestamp": "last_edited_time", "direction": "descending"}
    return paginate_all("POST", "/search", body=body, limit=args.limit or 20)


def cmd_get_page(args):
    return api_request("GET", f"/pages/{args.page_id}")


def cmd_get_db(args):
    return api_request("GET", f"/databases/{args.database_id}")


def cmd_get_ds(args):
    return api_request("GET", f"/data_sources/{args.data_source_id}")


def cmd_query(args):
    body = {}
    if args.filter:
        body["filter"] = json.loads(args.filter)
    if args.sort:
        body["sorts"] = json.loads(args.sort)

    params = {}
    if args.props:
        params["filter_properties[]"] = [p.strip() for p in args.props.split(",")]

    return paginate_all(
        "POST",
        f"/data_sources/{args.data_source_id}/query",
        body=body,
        params=params,
        limit=args.limit,
    )


def cmd_create_page(args):
    if not args.props and not args.props_file:
        print(json.dumps({"error": "Either --props or --props-file is required"}))
        sys.exit(1)
    props = json.load(open(args.props_file)) if args.props_file else json.loads(args.props)
    body = {
        "parent": {"data_source_id": args.data_source_id},
        "properties": props,
    }
    if args.template:
        body["template"] = {"type": args.template}

    result = api_request("POST", "/pages", body=body)
    if "error" in result:
        return result

    if args.template and args.wait_for_template:
        page_id = result.get("id")
        max_wait = int(args.wait_for_template)
        waited = 0
        while waited < max_wait:
            time.sleep(1)
            waited += 1
            blocks = api_request("GET", f"/blocks/{page_id}/children")
            if blocks.get("results"):
                result["_template_applied"] = True
                result["_template_wait_seconds"] = waited
                break
        else:
            result["_template_applied"] = False
            result["_template_wait_seconds"] = waited
    return result


def cmd_update_page(args):
    if not args.props and not args.props_file:
        print(json.dumps({"error": "Either --props or --props-file is required"}))
        sys.exit(1)
    props = json.load(open(args.props_file)) if args.props_file else json.loads(args.props)
    return api_request("PATCH", f"/pages/{args.page_id}", body={"properties": props})


def cmd_archive_page(args):
    return api_request("PATCH", f"/pages/{args.page_id}", body={"archived": True})


def cmd_get_blocks(args):
    params = {"page_size": min(args.limit, 100)} if args.limit else None
    return api_request("GET", f"/blocks/{args.block_id}/children", params=params)


def cmd_append_blocks(args):
    blocks = json.loads(args.blocks)
    return api_request("PATCH", f"/blocks/{args.page_id}/children", body={"children": blocks})


def main():
    parser = argparse.ArgumentParser(description="Notion API CLI for agents")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("discover")
    p.add_argument("--include-inline", action="store_true")

    p = sub.add_parser("search")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--type", choices=["page", "data_source"])
    p.add_argument("--limit", type=int)

    p = sub.add_parser("get-page")
    p.add_argument("page_id")

    p = sub.add_parser("get-db")
    p.add_argument("database_id")

    p = sub.add_parser("get-ds")
    p.add_argument("data_source_id")

    p = sub.add_parser("query")
    p.add_argument("data_source_id")
    p.add_argument("--filter")
    p.add_argument("--sort")
    p.add_argument("--limit", type=int)
    p.add_argument("--props")

    p = sub.add_parser("create-page")
    p.add_argument("data_source_id")
    p.add_argument("--props")
    p.add_argument("--props-file")
    p.add_argument("--template", choices=["default", "none"])
    p.add_argument("--wait-for-template", metavar="SECONDS", default="0")

    p = sub.add_parser("update-page")
    p.add_argument("page_id")
    p.add_argument("--props")
    p.add_argument("--props-file")

    p = sub.add_parser("archive-page")
    p.add_argument("page_id")

    p = sub.add_parser("get-blocks")
    p.add_argument("block_id")
    p.add_argument("--limit", type=int)

    p = sub.add_parser("append-blocks")
    p.add_argument("page_id")
    p.add_argument("--blocks", required=True)

    args = parser.parse_args()
    dispatch = {
        "discover": cmd_discover,
        "search": cmd_search,
        "get-page": cmd_get_page,
        "get-db": cmd_get_db,
        "get-ds": cmd_get_ds,
        "query": cmd_query,
        "create-page": cmd_create_page,
        "update-page": cmd_update_page,
        "archive-page": cmd_archive_page,
        "get-blocks": cmd_get_blocks,
        "append-blocks": cmd_append_blocks,
    }
    result = dispatch[args.command](args)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
