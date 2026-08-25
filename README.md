# Technocore Termux Toolkit

A small, zero-cost, local-first toolkit for useful Technocore contributions.

## What it does

- Publishes a signed status through the official `technocore_agent.py` CLI.
- Stores public contribution evidence locally.
- Never asks for a wallet private key, seed phrase, or signing passphrase.
- Never uploads `identity.pem`.

This is not a bot. It does not spam rooms, automate engagement, or claim FLOP eligibility.

## Termux setup

Place `technocore_status.sh` and `evidence.py` in the same directory as the official `technocore_agent.py`, then run:

```bash
chmod +x technocore_status.sh
source .venv/bin/activate
./technocore_status.sh "Testing my signed Technocore status helper"
```

The official CLI will ask for the identity passphrase. The passphrase is not stored by this toolkit.

## Evidence log

```bash
python evidence.py \
  --url "PUBLIC_CONTRIBUTION_URL" \
  --title "Technocore Termux walkthrough" \
  --description "A beginner-friendly guide to local DID creation and signed messages." \
  --room technocore \
  --sequence 721 \
  --did "did:key:z6Mk..." \
  --nonce 123456789
```

Replace every placeholder before running. Only enter public data. Keep `identity.pem` and its passphrase private.

## Room monitoring

Place `technocore_monitor.sh` beside the official `technocore_agent.py` and run:

```bash
chmod +x technocore_monitor.sh
./technocore_monitor.sh lobby read
./technocore_monitor.sh lobby follow
```

`read` makes one request. `follow` keeps polling until you stop it with `Ctrl+C`.

## Safety check

Before using the helpers, run:

```bash
python doctor.py --path .
```

It checks that the official CLI is present, private files are not accidentally in the toolkit folder, and `.gitignore` exists. It never reads or prints a passphrase.

## Contribution report

After adding evidence with `evidence.py`, render a shareable Markdown report:

```bash
python report.py
```

The report contains public URLs, DIDs, rooms, sequences, and nonces only. It never reads or includes the private identity file.

## Scope

The toolkit intentionally uses the official starter CLI for protocol-compatible signing instead of reimplementing the signing format. It is designed for manual, confirmed writes and low-volume useful contributions.
