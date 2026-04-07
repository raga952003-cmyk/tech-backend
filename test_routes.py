#!/usr/bin/env python3
"""Test script to verify auth routes are loaded"""

import sys
sys.path.insert(0, '.')

from app.api.auth import router

print("=" * 50)
print("AUTH ROUTER ROUTES:")
print("=" * 50)

for route in router.routes:
    print(f"Path: {route.path}")
    print(f"Methods: {route.methods}")
    print(f"Name: {route.name}")
    print("-" * 50)

print(f"\nTotal routes: {len(router.routes)}")
