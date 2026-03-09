---
title: "Going Paperless with Paperless-ngx: OCR, Auto-tagging, and Zero Paper Clutter"
date: 2026-03-09T22:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "Self-hosted document management on Raspberry Pi. OCR, auto-tagging, full-text search for all your documents."
categories: ["Homelab", "Automation"]
tags: ["paperless", "homelab", "raspberry-pi", "docker", "automation", "ocr", "self-hosted"]
cover:
  image: /images/covers/paperless-homelab.webp
  alt: "Paperless-ngx homelab setup"
---

I have a box. You probably have one too. It's full of papers: bank statements, insurance documents, tax returns, utility bills, contracts—the accumulated chaos of adult life. You keep it because "I might need this someday," but you never actually find anything in it. And when you do need that specific document from 2019? Good luck searching through 500 pages of chaos.

Two years ago I got tired of it. I set up Paperless-ngx on my Raspberry Pi homelab, and now I can find any document in 3 seconds by searching for a word, a date, or a correspondent name.

## What is Paperless-ngx?

Paperless-ngx is an open-source document management system. It's not a cloud storage tool (no syncing to someone else's servers), it's not a scanner app (though it integrates with mobile scanning), and it's not a fancy PDF reader. It's a full document pipeline: scan → OCR → tag → search.

The workflow is:

1. Scan document or take photo with phone
2. Drop into "consume" folder (watched by Paperless)
3. Paperless OCRs it (makes scanned images searchable)
4. Rules auto-tag it based on content/sender
5. Browse/search from the web interface
6. Old papers go in the recycling bin

That last step is the real magic. Once it's in Paperless with full-text search, you actually delete the physical paper.

## Docker Compose Setup on Raspberry Pi

My homelab is on a Raspberry Pi 4 with 8GB RAM and a 1TB USB SSD. Paperless is resource-intensive (OCR is CPU-heavy), but it's manageable.

Here's the Docker setup:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: securepassword
      POSTGRES_DB: paperless
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"
    environment:
      PAPERLESS_REDIS: redis://redis:6379
      PAPERLESS_DBHOST: postgres
      PAPERLESS_SECRET_KEY: generateareallylong_secret_key
      PAPERLESS_TIME_ZONE: Europe/Paris
      PAPERLESS_OCR_LANGUAGE: fra,eng
      PAPERLESS_OCR_USER_ARGS: '{"invalidate_upstream_cache": true}'
    volumes:
      - paperless_data:/usr/src/paperless/data
      - paperless_media:/usr/src/paperless/media
      - ./consume:/usr/src/paperless/consume
      - ./export:/usr/src/paperless/export
    restart: unless-stopped

  gotenberg:
    image: gotenberg/gotenberg:latest
    restart: unless-stopped

  tika:
    image: apache/tika:latest
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  paperless_data:
  paperless_media:
```

The `consume` folder is where Paperless watches for new documents. I have a scan script on my iPhone that automatically uploads PDFs here via a simple HTTP endpoint.

## The Magic: Auto-tagging Rules

Raw OCR is helpful, but auto-tagging is where the real power lives. Paperless can create rules based on document content, filename patterns, or sender information.

For example:

```python
# Rule 1: Bank statements
- Name: "Société Générale Bank Statements"
- Matches: Correspondent "Société Générale"
- Assign: Tag "banque", Document Type "bank-statement"

# Rule 2: Tax documents
- Name: "French Tax Authority"
- Matches: Content contains "impots.gouv.fr" OR Correspondent "Direction Générale des Finances"
- Assign: Tag "impôts", Document Type "tax-return"

# Rule 3: Insurance
- Name: "Insurance Documents"
- Matches: Correspondent contains "assurance" OR Content contains "police"
- Assign: Tag "assurance"

# Rule 4: Utilities
- Name: "EDF Power Bill"
- Matches: Correspondent "EDF"
- Assign: Tag "utilities", Tag "energy"
```

After tagging, searching is instant. Need all your 2024 tax documents? Click "impôts" tag. Looking for that specific insurance claim? Search "sinistre" and get results in milliseconds.

## The Consume Workflow

I have a shortcut on my iPhone that:

1. Opens the camera
2. Takes a photo of a document
3. Uploads it to my Paperless consume endpoint via HTTP POST
4. Shows a confirmation

Minutes later, the document is OCRed, tagged, and searchable.

For physical documents at my desk, I have a Brother ADS-3600W sheet-feed scanner that can scan directly to a shared SMB folder, which I've configured as a symlink to `consume/`. Drop a stack of 50 pages in, come back in 5 minutes, and they're all processed.

## Backup Strategy

Paperless data lives on the Pi's SSD, which is redundant (2x external drives with RAID), but I also back up to the cloud using `restic`:

```bash
#!/usr/bin/env bash
# Backup Paperless to Backblaze B2
restic backup /home/pi/paperless/data
restic backup /home/pi/paperless/media

# Prune old snapshots (keep last 30 days)
restic forget --keep-last 30 --prune
```

This runs nightly. If the Pi dies, I lose at most 24 hours of documents (and they're likely already in the consume folder waiting to be re-scanned anyway).

## The Real Impact

The best metric: I've actually deleted papers. Years of statements and old contracts went to recycling because I *knew* they were in Paperless. That's the psychological win. The box of chaos? Gone. Replaced by a single searchable database.

Finding documents went from "I'll deal with it later" to "found it in 3 seconds." That changes behavior. I scan things now instead of piling them up.

If you're still managing documents the analog way—storing boxes, losing receipts, panic-searching for contracts—Paperless-ngx is a weekend project that pays dividends for years. Self-hosted, open-source, and completely under your control.

Now go scan some chaos.
