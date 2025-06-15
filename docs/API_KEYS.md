# API Keys

This project relies on several third-party APIs. Populate the values in your `.env` file using the variables listed below. Some keys are optional while others are required for correct operation.

## Key Overview

| Service      | Environment variable      | Required? | Where to obtain the key | Typical free-tier limits |
|--------------|---------------------------|-----------|-------------------------|--------------------------|
| Pump.fun     | `PUMP_FUN_API_KEY`        | Optional  | Request access on the Pump.fun website (API is mostly undocumented and may require a session token). | ~100–200 requests per minute |
| Birdeye      | `BIRDEYE_API_KEY`         | Optional  | Create an account on [Birdeye](https://birdeye.so) and generate a token from the dashboard. | ~100–200 requests per minute |
| Dexscreener  | `DEXSCREENER_API_KEY`     | Optional  | Public API works without a key; you can request one via [Dexscreener docs](https://docs.dexscreener.io/) for higher limits. | ~10 requests/second per IP |
| Alchemy      | `ALCHEMY_API_KEY`         | Required* | Sign up at [Alchemy](https://www.alchemy.com) and create an application to obtain a project key. | 333,333 requests/month |
| Infura       | `INFURA_API_KEY`          | Required* | Sign up at [Infura](https://infura.io) and create a project to obtain a project ID. | 100,000 requests/day |
| Etherscan    | `ETHERSCAN_API_KEY`       | Required for deployer reputation checks | Generate an API key at [Etherscan](https://etherscan.io/myapikey). | 5 requests/second, 100,000/day |

`*` Either `ALCHEMY_API_KEY` or `INFURA_API_KEY` must be provided for Ethereum RPC calls.

If `ETHERSCAN_API_KEY` is missing, the bot will log a warning and skip deployer reputation checks instead of failing outright.

These limit values come from `docs/CLARIFICATIONS.md` and may change over time. Plan your polling frequency accordingly to avoid hitting free-tier quotas.
