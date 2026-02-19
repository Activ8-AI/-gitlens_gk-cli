#!/bin/bash

echo "Loading secrets..."
eval "$(python3 scripts/load_secrets_from_notion.py)"

echo "Starting MCP Relay Server..."
python3 orchestration/MCP/relay_server.py
