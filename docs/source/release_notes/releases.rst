========
Releases
========

.. towncrier release notes start

v4.4.0 (2020-12-24)
-------------------

Features
~~~~~~~~

- Introduces "Character Cards" a serializable identity abstraction and 'nucypher contacts' CLI to support. (`#2115 <https://github.com/nucypher/nucypher/issues/2115>`__)
- - nucypher cloudworkers now contains a complete and comprehensive set of features for easily managing, backing up and restoring one to many workers (`#2365 <https://github.com/nucypher/nucypher/issues/2365>`__)
- New composite gas strategy that uses the median from three different gas price oracles
  (currently, Etherchain, Upvest and gas-oracle.zoltu.io),
  which behaves more robustly against sporadic errors in the oracles (e.g., spikes, stuck feeds). (`#2420 <https://github.com/nucypher/nucypher/issues/2420>`__)
- Improve gas strategy selection: Infura users now can choose between ``slow``, ``medium`` and ``fast``, and a maximum gas price can be configured with --max-gas-price. (`#2445 <https://github.com/nucypher/nucypher/issues/2445>`__)


Bugfixes
~~~~~~~~

- Slowly try more and more nodes if some of the initial draft for a policy were inaccessible. (`#2416 <https://github.com/nucypher/nucypher/issues/2416>`__)
- Fix bad cli handling in several cloudworkers commands, improved envvar handling. (`#2475 <https://github.com/nucypher/nucypher/issues/2475>`__)


Misc
~~~~

-  (`#2244 <https://github.com/nucypher/nucypher/issues/2244>`__, `#2483 <https://github.com/nucypher/nucypher/issues/2483>`__)
- Solidity compilation refinements (`#2461 <https://github.com/nucypher/nucypher/issues/2461>`__)
- Deprecates internally managed geth process management (`#2466 <https://github.com/nucypher/nucypher/issues/2466>`__)
- Include checksum and IP addresses in exception messages for `Rejected`. (`#2467 <https://github.com/nucypher/nucypher/issues/2467>`__)
- Deprecates managed ethereum client syncing and stale interface methods (`#2468 <https://github.com/nucypher/nucypher/issues/2468>`__)
- Improves console messages for stakeholder CLI initialization and worker startup. (`#2474 <https://github.com/nucypher/nucypher/issues/2474>`__)
- Introduce a template to describe Pull Requests. (`#2476 <https://github.com/nucypher/nucypher/issues/2476>`__)


v4.3.0 (2020-12-08)
-------------------

Features
~~~~~~~~

- Introduces shorthand options for --bob-verifying-key (-bvk), --bob-encrypting-key (-bek) and alice verifying key (-avk) for CLI commands. (`#2459 <https://github.com/nucypher/nucypher/issues/2459>`__)
- Complete interactive collection of policy parameters via alice grant CLI. (`#2460 <https://github.com/nucypher/nucypher/issues/2460>`__)


Bugfixes
~~~~~~~~

- Corrected minimum stake value for --min-stake CLI option (`#2371 <https://github.com/nucypher/nucypher/issues/2371>`__)


Misc
~~~~

- Introduces a probationary period for policy creation in the network, until 2021-02-28 23:59:59 UTC. (`#2431 <https://github.com/nucypher/nucypher/issues/2431>`__)
- Supplies `AccessDenied` exception class for better incorrect password handling. (`#2451 <https://github.com/nucypher/nucypher/issues/2451>`__)
- Maintain compatibility with python 3.6 (removes re.Pattern annotations) (`#2458 <https://github.com/nucypher/nucypher/issues/2458>`__)


v4.2.1 (2020-12-04)
-------------------

Bugfixes
~~~~~~~~

- Removes tests import from constants module causing pip installed versions to crash. (`#2452 <https://github.com/nucypher/nucypher/issues/2452>`__)


v4.2.0 (2020-12-03)
-------------------

Features
~~~~~~~~

- Improve user experience when removing unused substakes (CLI and docs). (`#2450 <https://github.com/nucypher/nucypher/issues/2450>`__)


Bugfixes
~~~~~~~~

- Fix bug in deployer logic while transferring ownership of StakingInterfaceRouter (`#2369 <https://github.com/nucypher/nucypher/issues/2369>`__)
- Allow arbitrary decimal precision when entering NU amounts to nucypher CLI. (`#2441 <https://github.com/nucypher/nucypher/issues/2441>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Document usage of hardware wallets for signing. (`#2346 <https://github.com/nucypher/nucypher/issues/2346>`__)
- Improvements to the staking guide: extending description of winddown command, other minor corrections. (`#2434 <https://github.com/nucypher/nucypher/issues/2434>`__)


Misc
~~~~

- Rework internal solidity compiler usage to implement "Standard JSON Compile". (`#2439 <https://github.com/nucypher/nucypher/issues/2439>`__)
- Introduces `--config-path` and `--logging-path` CLI flags displaying default nucypher directories (`#2446 <https://github.com/nucypher/nucypher/issues/2446>`__)


v4.1.2 (2020-11-09)
-------------------

Features
~~~~~~~~

- Added support for a user-provided gas price to the ``nucypher stake`` command, using ``--gas-price GWEI``. (`#2425 <https://github.com/nucypher/nucypher/issues/2425>`__)


Bugfixes
~~~~~~~~

- Correct CLI problems when setting the min fee rate. Also, simplifies usage by expressing rates in GWEI. (`#2390 <https://github.com/nucypher/nucypher/issues/2390>`__)
- Tone-down learning logging messages even more (see issue #1712). Fixes some CLI and exception messages. (`#2395 <https://github.com/nucypher/nucypher/issues/2395>`__)
- Fixes logical bug in ``WorkTracker`` to ensure commitment transactions can only be issued once per period. (`#2406 <https://github.com/nucypher/nucypher/issues/2406>`__)
- Removes leftover imports of Twisted Logger, using instead our shim (Closes #2404). Also, changes NuCypher Logger behavior to always escape curly braces. (`#2412 <https://github.com/nucypher/nucypher/issues/2412>`__)
- Now ``BlockchainInterface.gas_strategy`` always has a value; previously it was possible to pass ``None`` via the constructor (e.g. if the config file had an explicit ``"null"`` value). (`#2421 <https://github.com/nucypher/nucypher/issues/2421>`__)
- Take advantage of the changes in PR#2410 by retrying worker commitments on failure (`#2422 <https://github.com/nucypher/nucypher/issues/2422>`__)
- Domain "leakage", or nodes saving metadata about nodes from other domains (but never being able to verify them) was still possible because domain-checking only occurred in the high-level APIs (and not, for example, when checking metadata POSTed to the node_metadata_exchange endpoint).  This fixes that (fixes #2417).

  Additionally, domains are no longer separated into "serving" or "learning".  Each Learner instance now has exactly one domain, and it is called domain. (`#2423 <https://github.com/nucypher/nucypher/issues/2423>`__)


Misc
~~~~

- Updates contract registry after upgrade of StakingEscrow to v5.5.1, at behest of the DAO (proposal #0). (`#2402 <https://github.com/nucypher/nucypher/issues/2402>`__)
- Improved newsfragments README file to clarify release note entry naming convention. (`#2415 <https://github.com/nucypher/nucypher/issues/2415>`__)


v4.1.1 (2020-10-29)
-------------------

Features
~~~~~~~~

- Add CLI functionality for the removal of unused (inactive) sub-stakes. Depending on the staker's sub-stake configuration, this command can reduce the associated worker's gas costs when making commitments. (`#2384 <https://github.com/nucypher/nucypher/issues/2384>`__)


Bugfixes
~~~~~~~~

- Automatically restart Ursula worker task on failure. (`#2410 <https://github.com/nucypher/nucypher/issues/2410>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Update global fee range documentation, including genesis values. (`#2363 <https://github.com/nucypher/nucypher/issues/2363>`__)


Misc
~~~~

- Update Ursula network grant availability script for mainnet usage. (`#2383 <https://github.com/nucypher/nucypher/issues/2383>`__)
- GitHub Action to ensure that each pull request into main makes an associated release note entry. (`#2396 <https://github.com/nucypher/nucypher/issues/2396>`__)


v4.1.0 (2020-10-19)
-------------------

Bugfixes
~~~~~~~~

- Temporary workaround for lack of single attribute for the value of "domain" in sprouts and mature nodes. (`#2356 <https://github.com/nucypher/nucypher/issues/2356>`__)
- Show the correct fleet state on Ursula status page. (`#2368 <https://github.com/nucypher/nucypher/issues/2368>`__)
- Don't crash when handling failed transaction; reduce network learning messages. (`#2375 <https://github.com/nucypher/nucypher/issues/2375>`__)
- Reduce the greediness of prometheus metrics collection. (`#2376 <https://github.com/nucypher/nucypher/issues/2376>`__)
- Ensure minimum NU stake is allowed instead of stake creation failing for not enough tokens. (`#2377 <https://github.com/nucypher/nucypher/issues/2377>`__)
- Fixes to status page based on reworked design done in PR #2351. (`#2378 <https://github.com/nucypher/nucypher/issues/2378>`__)
- Track pending Ursula commitment transactions due to slower gas strategies. (`#2389 <https://github.com/nucypher/nucypher/issues/2389>`__)


v4.0.1 (2020-10-14)
-------------------

Misc
~~~~

- Set default teacher uri for mainnet. (`#2367 <https://github.com/nucypher/nucypher/issues/2382>`__)


v4.0.0 (2020-10-14)
-------------------

**🚀 Mainnet Launch 🚀**
