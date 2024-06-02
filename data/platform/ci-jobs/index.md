---

title: "Data Team CI Jobs"
description: "GitLab Data Team CI Jobs"
---









---

This page documents the CI jobs used by the data team in Merge Requests in both the [Data Tests](https://gitlab.com/gitlab-data/data-tests) and [Analytics](https://gitlab.com/gitlab-data/analytics) projects.

## What to do if a pipeline fails

- If a weekend has passed re-run any CLONE steps which were performed prior, every Sunday (5:00AMUTC) all old pipeline databases are [dropped](https://gitlab.com/gitlab-data/analytics/-/blob/master/orchestration/drop_snowflake_objects.py) from SnowFlake older than 14 days.
![ci-db-deletion-schema.png](ci-db-deletion-schema.png)
- Merge master branch. Due to how dbt handles packages pipelines can fail due to package failures which should always be handled in the latest branch.
- Confirm [model selection syntax](https://docs.getdbt.com/reference/node-selection/syntax). In general, it is easiest to simply use the file names of the models you are changing.
- If still uncertain or facing any issues, request assistance in the #data Slack channel

### Variable Name not found in the CI Pipeline job

This kind of error pops up in the pipeline like KeyError: 'GITLAB_COM_CI_DB_USER'. It means the variable is not defined in the variable section of CI/CD Settings. To resolve this, add the variable name to [CI/CD setting](https://gitlab.com/gitlab-data/analytics/-/settings/ci_cd) i.e. settings --> ci_cd --> variable, also provide the variable value.
**Notes:-** Turn off the Flags, so the variable is accessible from the CI pipeline.
The same applies to the variable value; if it is incorrect in the job, we can update it in the above link.

## Analytics pipelines

## Stages

CI jobs are grouped by stages.

### ❄️ Snowflake

These jobs are defined in [`.gitlab-ci.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/.gitlab-ci.yml). All Snowflake objects created by a CI clone job will exist until dropped, either manually or by the [weekly clean up of Snowflake objects](/handbook/business-technology/data-team/platform/ci-jobs/#what-to-do-if-a-pipeline-fails).

#### `clone_prep_specific_schema`

Run this if you need a clone of any schema available in the prep database. Specify which schema to clone with the `SCHEMA_NAME` variable. If the clone already exists, this will do nothing.

#### `clone_prod_specific_schema`

Run this if you need a clone of any schema available in the prod database. Specify which schema to clone with the `SCHEMA_NAME` variable. If the clone already exists, this will do nothing.

#### `clone_prod`

Runs automatically when the MR opens to be able to run any dbt jobs. Subsequent runs of this job will be fast as it only verifies if the clone exists. This is an empty clone of the `prod` and `prep` databases.

#### `clone_prod_real`

Run this if you need to do a real clone of the `prod` and `prep` databases. This is a full clone both databases.

#### `clone_raw_full`

Run this if you need to run extract, freshness, or snapshot jobs. Subsequent runs of this job will be fast as it only verifies if the clone exists.

#### `clone_raw_postgres_pipeline`

Run this if you only need a clone of the raw `tap_postgres` schema in order to test changes to postgres pipeline or a manifest file.  If the raw clone already exists, this will do nothing.

#### `clone_raw_sheetload`

Run this if you only need a clone of the raw `sheetload` schema in order to test changes or additions to sheetload.  If the raw clone already exists, this will do nothing.

#### `clone_raw_specific_schema`

Run this if you need a clone of any other raw schema in order to test changes or additions. Specify which raw schema to clone with the `SCHEMA_NAME` variable. If the raw clone already exists, this will do nothing.

#### `clone_raw_by_schema`

Clones the entire RAW DB, created due to timeout issues when trying to clone the DB using SF commands.

**NB Due to the size of the DB created by running, only run this when you absolutely have to run through complete platform tests. Likely only applicable for infrastructure upgrades.**

#### `force_clone_both`

Run this if you want to force refresh raw, prod, and prep. This does a full clone of raw, but a shallow clone of `prep` and `prod`.

#### `🔑grant_clones`

Run this if you'd like to grant access to the copies or clones of `prep` and `prod` for your branch to your role or a role of a business partner. Specify the snowflake role (see [roles.yml](https://gitlab.com/gitlab-data/analytics/-/blob/master/permissions/snowflake/roles.yml)) you'd like to grant access to using the `GRANT_TO_ROLE` variable. This job grants the same `select` permissions as the given role has in `prep` and `prod` for all database objects within the clones of `prep` and `prod`. It does not create any future grants and so **all relevant objects must be built in the clone before you run this job if you want to ensure adequate object grants.**

***Since grants are copied from production database permissions, these grants cannot be run on new models.*** If access is needed to new models, permission can be granted by a Data Engineer after the 🔑 `grant_clones` CI job has completed successfully. Instructions for the Data Engineer can be found in [runbooks/CI_clones](https://gitlab.com/gitlab-data/runbooks/-/tree/main/CI_clones).

**This will be fastest if the Data Engineer is provided with:**

1. the fully qualified name (`"database".schema.table`) of the table(s) to which access needs to be granted
2. the role to which permissions should be granted

The database names for `PREP` and `PROD` can be found in the completed 🔑 `grant_clones` CI job. Linking this job for the DE will also be helpful in expediting this process.

### 🚂 Extract

These jobs are defined in [`extract-ci.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/extract/extract-ci.yml)

#### `boneyard_sheetload`

Run this if you want to test a new boneyard sheetload load. This requires the real `prod` and `prep` clones to be available.

#### `sheetload`

Run this if you want to test a new sheetload load. This jobs runs against the clone of `RAW`. Requires the `clone_raw_specific_schema` (parameter `SCHEMA_NAME=SHEETLOAD`) job to have been run.

#### `🛢 saas_pgp_test`

This pipeline needs to be executed when doing changes to any of the below manifest files present in path `analytics/extract/postgres_pipeline/manifests`.

- el_saas_customers_scd_db_manifest.yaml
- el_saas_gitlab_com_ci_db_manifest.yaml
- el_saas_gitlab_com_ci_scd_db_manifest.yaml
- el_saas_gitlab_com_db_manifest.yaml
- el_saas_gitlab_com_scd_db_manifest.yaml

This pipeline requires.

1. Clone of `TAP_POSTGRES` schema(Mandatory): The `TAP_POSTGRES` schema can be cloned by using CI JOB `clone_raw_postgres_pipeline` which is part of `❄️ Snowflake`.
2. Variable `MANIFEST_NAME`(Mandatory): The value is manifest yaml filename except postfix `_db_manifest.yaml`, For example if modified file is `el_gitlab_com_ci_db_manifest.yaml` the variable passed will be `MANIFEST_NAME`=`el_saas_gitlab_com_ci`.
3. Variable `TASK_INSTANCE`(Optional): This do not apply to any of the incremental table. It is only required to be passed for table listed in the SCD manifest file for who has `advanced_metadata` flag value set to `true`. For example for table `bulk_import_entities` in manifest file `el_saas_gitlab_com_scd_db_manifest.yaml`. We need to pass this variable `TASK_INSTANCE`. For testing purpose this can be any unique identifiable value.

#### `gitlab_ops_pgp_test`

This pipeline needs to be executed when doing changes to any of the below manifest files present in path `analytics/extract/postgres_pipeline/manifests_decomposed`.

- el_gitlab_ops_db_manifest.yaml
- el_gitlab_ops_scd_db_manifest.yaml

**This is separate from the `pgp_test` job because it requires a CloudSQL Proxy to be running in order to connect to the gitlab-ops database.**

This pipeline requires.

1. Clone of `TAP_POSTGRES` schema(Mandatory): The `TAP_POSTGRES` schema can be cloned by using CI JOB `clone_raw_postgres_pipeline` which is part of `❄️ Snowflake`.
2. Variable `MANIFEST_NAME`(Mandatory): The value is manifest yaml filename except postfix `_db_manifest.yaml`, For example if modified file is `el_gitlab_ops_db_manifest.yaml` the variable passed will be `MANIFEST_NAME`=`el_gitlab_ops`.
3. Variable `TASK_INSTANCE`(Optional): This do not apply to any of the incremental table. It is only required to be passed for table listed in the SCD manifest file for who has `advanced_metadata` flag value set to `true`. For example for table `ci_builds` in manifest file `el_gitlab_ops_scd_db_manifest.yaml`. We need to pass this variable `TASK_INSTANCE`. For testing purpose this can be any unique identifiable value.

### ⚙️ dbt Run

These jobs are defined in [`snowflake-dbt-ci.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/snowflake-dbt-ci.yml)

> As part of a DBT Model Change MR, you need to trigger a pipeline job to test that your changes won't break anything in production. To trigger these jobs, go to the "Pipelines" tab at the bottom of this MR and click on the appropriate stage (dbt_run or dbt_misc).

These jobs are scoped to the `ci` target. This target selects a subset of data for the snowplow and version datasets.

Note that job artifacts are available for all dbt run jobs. These include the compiled code and the run results.

These jobs run against the primary `RAW` database.

Most dbt run jobs can be parameterized with a variable specifying dbt model that requires testing.

The variable `SELECTION` is a stand-in for any of the examples in [the dbt documentation on model selection syntax](https://docs.getdbt.com/docs/model-selection-syntax#section-specifying-models-to-run).

If you are testing changes to tests in the `data-tests` project, you can pass in `DATA_TEST_BRANCH` to the manual jobs along with the branch name. This will update the branch in the `packages.yml` for the data-tests package. This works for any job running `dbt test`.

You can also add `--fail-fast` to the end of the model selection to quickly end the dbt call at the first failure. Read the [dbt docs](https://docs.getdbt.com/reference/commands/run#failing-fast) for more information.

Available selectors can be found in the [selector.yml](https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/selectors.yml) file. The dbt build command will run all seeds, snapshots, models, and tests that are part of the selection. This is useful for the following scenarios:

- Testing of new selectors for Airflow DAGs
- Testing version upgrades to the dbt environment

#### DBT CI Job size

If you want to run a dbt job via the `🏗️🏭build_changes` or `🎛️custom_invocation`, you have the possibility to choose the size of the Snowflake warehouse you want to use in the CI job. Starting with XS, followed by L and last you can select XL size warehouse. This can be done by setting the `WAREHOUSE` variable when starting the CI job:

- Setting `WAREHOUSE` to `DEV_XS` is will use an `XS` warehouse.
- Setting `WAREHOUSE` to `DEV_L` is will use a `L` warehouse.
- Setting `WAREHOUSE` to `DEV_XL` is will use an `XL` warehouse.

Using a bigger warehouse will result in shorter run time (and prevents timing out of large models),
but also results in bigger costs for GitLab if the warehouse is running for less than a minute.
Reference your local development run times and model selection to aid in identifying what warehouse should be used.
If you are unsure or are unable to have a reasonable estimation of the run time start with a `L` warehouse.
Also its important to find parity between testing a model and how the model is executed in Production.
Of course there can be a good reason to use a bigger warehouse,
if there are complex transformations or lots of data to be processed more power is required.
But always also please check your model. Maybe the model can be adjusted to run more efficiently.
Running your test on a bigger warehouse will not only trigger increased costs for **this** CI Job,
but it also could run inefficiently in production and could have a much bigger impact for the long run.

#### `🏗️🏭build_changes`

This job is designed to work with most dbt changes without user configuration.  It will clone, run, and test the new and changed models referencing the live database, `PROD`, `PREP`, and `RAW`, for any tables that have not been changed based on the most recent version of the [dbt documentation](https://dbt.gitlabdata.com/).  If the job fails it should represent an issue within the code itself and should be addressed by the developer making the changes.

Should the changes made fall outside the default selection of this job, it can be configured in the following ways:

- `WAREHOUSE`: Defaults to `DEV_XL` but will accept `DEV_XS` and `DEV_L` as well.
- `SELECTION`: Defaults to a list of any changed SQL or CSV files but accepts any valid dbt selection statement.
- `DOWNSTREAM`: Defaults to `None` but will accept the `plus` and `n-plus` operators. Has no impact when overriding the `SELECTION`. See the [documentation](https://docs.getdbt.com/reference/node-selection/graph-operators) for the graph operators for details on what each will do.
- `FAIL_FAST`: Defaults to `True` but accepts `False` to continue running even if a test fails or a model can not build.  See the [documentation](https://docs.getdbt.com/reference/global-configs/failing-fast) for additional details.
- `EXCLUDE`: Defaults to `None` but will accept any dbt node selection. See the [documentation](https://docs.getdbt.com/reference/node-selection/exclude) for additional details.
- `FULL_REFRESH`: Defaults to `False` but accepts `True` to re-clone and rebuild any tables that would otherwise run in an incremental state. See the [documentation](https://docs.getdbt.com/reference/commands/run#refresh-incremental-models) for additional details.
- `VARS`: Defaults to `None` but will accept a comma separated list of quoted key value pairs. e.g. `"key1":"value1","key2":"value2"`.
- `RAW_DB`: Defaults to `Live` but will accept `Dev`.  Selecting `Dev` will have the job use the branch specific version of the live `RAW` database, only the data that is explicitly loaded will be present.  This is needed when testing models build on extracts that are new in the same branch.

<details markdown="1">
<summary>Cross-Walk</summary>

|Change Examples |    Previous CI Process |    New CI Process|
| --- | --- | --- |
| Add column to small table or view | <ol><li>🏗️🔆run_changed_️clone_model_dbt_select</li><ul><li>ANCESTOR_TYPE : +</li></ul><li>🏗🛺️run_changed_models_sql</li></ol> | <ol><li>🏗️🏭build_changes</li><ul><li>WAREHOUSE : DEV_XS</li></ul></ol> |
| Update column description    | <ol><li>📚✏️generate_dbt_docs</li></ol> |    <ol><li>📚✏️generate_dbt_docs</li></ol> |
| Update or create a small dbt snapshot    | <ol><li>🥩clone_raw_full</li><li>🐭🥩specify_raw_model</li><ul><li>DBT_MODELS : snapshot_name</li></ul></ol> |    <ol><li>🏗️🏭build_changes</li><ul><li>WAREHOUSE : DEV_XS</li></ul></ol> |
| Add or update a seed |    <ol><li>🌱specify_csv_seed</li><ul><li>DBT_MODELS : seed_name</li></ul></ol> |    <ol><li>🏗️🏭build_changes</li><ul><li>WAREHOUSE : DEV_XS</li><li>FULL_REFRESH : True</li></ul></ol> |
| Update a model and test downstream impact |    <ol><li>🏗️🔆run_changed_️clone_model_dbt_select</li><ul><li>DEPENDANT_TYPE : +</li><li>ANCESTOR_TYPE: +1</li></ul><li>🏗🛺️run_changed_models_sql</li><ul><li>DEPENDANT_TYPE : +</li></ul></ol> |    <ol><li>🏗️🏭build_changes</li><ul><li>WAREHOUSE : DEV_XS</li><li>DOWNSTREAM : +</li></ul></ol> |
| Update a model and test specific models    | <ol><li>🔆⚡️clone_model_dbt_select</li><ul><li>DBT_MODELS : 1+specific_models+1</li></ul><li>🐭specify_model</li><ul><li>DBT_MODELS : specific_models+1</li></ul></ol> |    <ol><li>🏗️🏭build_changes</li><ul><li>WAREHOUSE : DEV_XS</li><li>SELECTION : specific_models+1</li></ul></ol> |
| Make a chance to an incremental model without full refresh |    <ol><li>🏗️🔆run_changed_️clone_model_dbt_select</li><ul><li>ANCESTOR_TYPE : +</li></ul><li>🏗️🛺🐘run_changed_models_sql_xl</li><ul><li>REFRESH : ' ' </li></ul></ol>| <ol><li>🏗️🏭build_changes</li></ul></ol> |
| Make a chance to an incremental model with full refresh |    <ol><li>🏗️🔆run_changed_️clone_model_dbt_select</li><ul><li>ANCESTOR_TYPE : +</li></ul><li>🏗️🛺🐘run_changed_models_sql_xl</li></ol> |    <ol><li>🏗️🏭build_changes</li><ul><li>FULL_REFRESH : True</li></ul></ol>|
| Update a model and test downstream impact. skipping specific model     | <ol><li>🏗️🔆run_changed_️clone_model_dbt_select</li><ul><li>DEPENDANT_TYPE : +</li><li>ANCESTOR_TYPE: +1</li></ul><li>🐘specify_xl_model</li><ul><li>DBT_MODELS : specific_model+ --exclude other_model</li></ul></ol> |    <ol><li>🏗️🏭build_changes</li><ul><li>EXCLUDE : other_model</li><li>DOWNSTREAM : +</li></ul></ol> |
| Change a model that needs vars |    NA    | <ol><li>🏗️🏭build_changes</li><ul><li>VARS : "key1":"value1","key2":"value2"</li></ul></ol> |
| Make a change and see all errors |    <ol><li>🏗️🔆run_changed_️clone_model_dbt_select</li><ul><li>ANCESTOR_TYPE : +</li></ul><li>🏗🛺️run_changed_models_sql</li></ol> |    <ol><li>🏗️🏭build_changes</li><ul><li>WAREHOUSE : DEV_XS</li><li>FAIL_FAST : False</li></ul></ol> |
| Make a changes to or useing a Selector |    <ol><li>➕🐘🏭⛏specify_selector_build_xl</li><ul><li>DBT_SELECTOR : customers_source_models</li></ul></ol> |    <ol><li>🎛️custom_invocation</li><ul><li>STATEMENT : build --selector customers_source_models</li></ul></ol> |
| Add a model built on a new Sheetload in the same MR |    <ol><li>❄️ Snowflake: clone_raw_sheetload</li><li>Extract: sheetload</li><li>specify_raw_model</li><ul><li>DBT_MODELS : sheetload_file_name_source</li></ul></ol> |    <ol><li>❄️ Snowflake: clone_raw_sheetload</li><li>Extract: sheetload</li><li>🏗️🏭build_changes</li><ul><li>RAW_DB : Dev</li></ul></ol> |

</details>

#### `🎛️custom_invocation`

This job is designed to be a way to resolve edge cases not fulfilled by other pre-configured jobs.  The job will process the provided dbt command using the selected warehouse.  For `defer` commands the reference `manifest.json` can referenced at using `--state reference_state`.

This job can be configured in the following ways:

- `WAREHOUSE`: No default, a value of `DEV_XL`, `DEV_L`, or `DEV_XS` must be provided.
- `STATEMENT`: No default, a complete `dbt` statement must be provided. e.g. `run --select +dim_date`.

#### `📚📝generate_dbt_docs`

You should run this pipeline manually when either `*.md` or `.yml` files are changed under `transform/snowflake-dbt/` folder. The motivation for this pipeline is to check and validate changes in the `dbt` documentation as there is no check on how the documentation was created - errors are allowed and not validated, by default. There are no parameters for this pipeline.

### 🛠 dbt Misc

These jobs are defined in [`snowflake-dbt-ci.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/snowflake-dbt-ci.yml)

#### `🧠all_tests`

Runs all the tests

- Note: it is not necessary to run this job if you've run any of the dbt_run stage jobs as tests are included.

#### `💾data_tests`

Runs only data tests

#### `🔍tableau_direct_dependencies_query`

This job runs automatically and only appears when `.sql` files are changed. In its simplest form, the job will check to see if any of the currently changed models are **directly** connected to tableau views, tableau data-extracts and/or tableau flows. If they are, the job will fail with a notification to check the relevant dependency. If it is not queried, the job will succeed.

Current caveats with the job are:

- It will not tell you which tableau workbook to check
- It will not tell indirectly connected downstream dependencies. This feature will be a part of upcoming iteration to this job.

##### Explanation

This section explains how the `tableau_direct_dependencies_query` works.

`git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD --name-only | grep -iEo "(.*)\.sql" | sed -E 's/\.sql//' | awk -F '/' '{print tolower($NF)}' | sort | uniq`

This gets the list of files that have changed from the master branch (i.e. target branch) to the current commit (HEAD). It then finds (grep) only the sql files and substitutes (sed) the `.sql` with an empty string. Using `awk`, it then prints the lower-case of the last column of each line in a file (represented by $NF - which is the number of fields), using a slash (/) as a field separator. Since the output is directory/directory/filename and we make the assumption that most dbt models will write to a table named after its file name, this works as expected. It then sorts the results, gets the unique set and is then used by our script to check the downstream dependencies.

`orchestration/tableau_dependency_query/src/tableau_query.py`

We leverage [Monte Carlo](/handbook/business-technology/data-team/platform/monte-carlo/) to detect downstream dependencies which is also our data obeservability tool. Using [Monte carlo API](https://apidocs.getmontecarlo.com/) we detect directly connected downstream nodes of type `tableau-view`, `tableau-published-datasource-live`, `tableau-published-datasource-extract` using the [`GetTableLineage` GraphQL endpoint](https://apidocs.getmontecarlo.com/#query-getTableLineage).

If no dependencies are found for the model, then you would get an output in the CI jobs logs - `INFO:root:No dependencies returned for model <model_name>` and the job will be marked as successful.

And if dependencies were found for the model, then the job would fail with the value error `ValueError: Check these models before proceeding!`. The job logs will contain number of direct dependencies found for a given model, type of tableau object, tableau resource name and monte carlo asset link, in the below format:

```bash
Found <number of tableau dependencies> downstream dependencies in Tableau for the model <model name>
INFO:root: <tableau resource type> : <name of tableau resource> - : <monte_carlo_connection_asset_url>
ValueError: Check these models before proceeding!
ERROR: Job failed: command terminated with exit code 1
```

More implementation details can be found in the issue [here](https://gitlab.com/gitlab-data/analytics/-/issues/19885).

#### `🛃dbt_sqlfluff`

Runs the SQLFluff linter on all changed `sql` files within the `transform/snowflake-dbt/models` directory.  This is currently executed manually and is allowed to fail, but we encourage anyone developing dbt models to view the output and format according to the linters specifications as this format will become the standard.

#### `🚫safe_model_script`

In order to ensure that all [SAFE](/handbook/legal/safe-framework/) data is being stored in appropriate schemas all models that are downstream of [source models with MNPI data](/handbook/business-technology/data-team/how-we-work/new-data-source/#mnpi-data) must either have an exception tag or be in a restricted schema in `PROD`. This CI Job checks for compliance with this state. If your MR fails this job it will likely either need to be audited and verified to be without change MNPI data and have the appropriate exception tags added, or models may need to be migrated to the appropriate restricted schema

#### `🔍macro_name_check`

Automatically runs when making changes in the snowflake-dbt/macros folder and checks if the newly created macros match the correct name format.

#### `🗂schema_tests`

Runs only schema tests

#### `📸snapshots`

Runs snapshots. This jobs runs against the clone of `RAW`. Requires the `clone_raw_full` job to have been run.

#### `📝specify_tests`

Runs specified model tests with the variable `DBT_MODELS`

#### `🌱manual_seed`

Runs a full seed operation. For use to confirm results when working on changes to the dbt seeds themselves.

### 🐍 Python

These jobs are defined in [`.gitlab-ci.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/.gitlab-ci.yml).

There are several jobs that only appear when `.py` files have changed. All of them will run automatically on each new commit where `.py` files are present.

Pipelines running automatically are:

#### `⚫python_black`

We handle python code formatting using the [`black`](https://github.com/psf/black) library. The pipeline checks the entire `/analytics` repo (all `*.py` files).

#### `✏️python_mypy`

We use the [`mypy`](https://mypy.readthedocs.io/en/stable/) library to check code correctness. The pipeline checks the entire `/analytics` repo (all `*.py` files).

#### `🗒️python_pylint`

We use the [`pylint`](https://pylint.pycqa.org/en/latest/) library and check code linting for Python files. The pipeline checks only **changed** Python files (`*.py`) in `/analytics` repo.

#### `🌽python_flake8`

We use the [`flake8`](https://flake8.pycqa.org/en/latest/) library and check code linting for Python files. The pipeline checks only **changed** Python files (`*.py`) in `/analytics` repo.

#### `🦅python_vulture`

We use the [`vulture`](https://pypi.org/project/vulture/0.5/) library and check unused for Python files. `Vulture` finds unused classes, functions and variables in your code. This helps you cleanup and find errors in your programs.
The pipeline checks only **changed** Python files (`*.py`) in `/analytics` repo.

#### `🤔python_complexity`

We use the [`xenon`](https://pypi.org/project/xenon/) library and check code complexity for Python files. The pipeline checks the entire `/analytics` repo (all `*.py` files).

#### `✅python_pytest`

We ensure code quality by running the [`pytest`](https://docs.pytest.org/en/7.1.x/contents.html) library and test cases in `/analytics` repo. The pipeline all test files in the entire `/analytics` repo (all `*.py` files contains `pytest` library).

Manually running pipelines are:

#### `🧊⚙permifrost_run`

Manual job to do a dry run of [Permifrost](https://gitlab.com/gitlab-data/permifrost/).

#### `🧊 permifrost_spec_test`

Must be run at least once before any changes to `permissions/snowflake/roles.yml` are merged. Takes around 30 minutes to complete.

Runs the `spec-test` cli of [Permifrost](https://gitlab.com/gitlab-data/permifrost/) to verify changes have been correctly configured in the database.

#### `📁 yaml_validation`

Triggered when there is a change to `permissions/snowflake/roles.yml`. Validates that the YAML is correctly formatted.

#### `snowflake_provisioning_snowflake_users`

This job adds/removes specified users and roles directly in Snowflake based on changes to `snowflake_users.yml`.

##### Quick Summary

- To add new users/roles in Snowflake, add the new username(s) to [`snowflake_users.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/permissions/snowflake/snowflake_users.yml?ref_type=heads).
- To create a development database for new users, add the CI variable `IS_DEV_DB: True`.

<details><summary>Further Explanation</summary>

##### Further Explanation

Under the hood, this CI job is calling the python script [`orchestration/snowflake_provisioning_automation/provision_users/provision_user.py`](https://gitlab.com/gitlab-data/analytics/-/blob/master/orchestration/snowflake_provisioning_automation/provision_users/provision_users.py?ref_type=heads).

These are the full list of CI job arguments, all are **OPTIONAL**:

1. `IS_TEST_RUN`:
    - Defaults to `False`, but accepts `True`.
    - If True, will only **print** the `GRANT` sql statements, but will not run them.
1. `USERS_TO_ADD`:
    - Defaults to the usernames **added** to [`snowflake_users.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/permissions/snowflake/snowflake_users.yml?ref_type=heads) within the MR.
    - To override, pass in a string value like so `USERS_TO_ADD: username_to_add1 username_to_add2`
1. `IS_DEV_DB`:
    - Defaults to `False`, but accepts `True`.
    - If True, will create development databases for each username in `usernames_to_add`.

Note: `USERS_TO_REMOVE` argument is not available for this job because all deactivated users will be removed in Snowflake via separate airflow job.
</details>

#### `snowflake_provisioning_roles_yaml`

This job updates `roles.yml` automatically based on changes to `snowflake_users.yml`.

##### Quick Summary

- To add new user entries to `roles.yml`, add the new username(s) to [`snowflake_users.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/permissions/snowflake/snowflake_users.yml?ref_type=heads).
- Likewise, to remove user entries from `roles.yml`, delete the username(s) from [`snowflake_users.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/permissions/snowflake/snowflake_users.yml?ref_type=heads).
- If no optional arguments are passed into the CI job, it will run with the default arguments described in [Automating roles.yml: Common Templates](/handbook/business-technology/data-team/platform/#common-custom-templates) section of the handbook.

<details><summary>Further Explanation</summary>

##### Further explanation

Under the hood, this CI job is calling the python script [`orchestration/snowflake_provisioning_automation/update_roles_yaml/update_roles_yaml.py`](https://gitlab.com/gitlab-data/analytics/-/blob/master/orchestration/snowflake_provisioning_automation/update_roles_yaml/update_roles_yaml.py?ref_type=heads).

These are the full list of CI job arguments, all are **OPTIONAL**:

1. `IS_TEST_RUN`:
    - Defaults to `False`, but accepts `True`.
    - If True, will only **print** what values will be added to `roles.yml`
1. `USERS_TO_ADD`:
    - Defaults to the usernames **added** to [`snowflake_users.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/permissions/snowflake/snowflake_users.yml?ref_type=heads) within the MR.
    - To override, pass in a string value like so `USERS_TO_ADD: username_to_add1 username_to_add2`
1. `USERS_TO_REMOVE`:
    - Defaults to the usernames **removed** from [`snowflake_users.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/permissions/snowflake/snowflake_users.yml?ref_type=heads) within the MR.
    - To override, pass in a string value like so `USERS_TO_REMOVE: username_to_remove1 username_to_remove2`
1. `DATABASES_TEMPLATE`:
    - Defaults to None, but accepts any JSON string, see this ['Databases' handbook section](/handbook/business-technology/data-team/platform/#databases) for more details/examples.
1. `ROLES_TEMPLATE`:
    - Defaults to 'SNOWFLAKE_ANALYST' role and 'DEV_XS' warehouse, but accepts any JSON string, see this ['Roles' handbook section](/handbook/business-technology/data-team/platform/#roles) for more details/examples.
1. `USERS_TEMPLATE`:
    - Defaults to the standard user entry, see ['Users' handbook section](/handbook/business-technology/data-team/platform/#users) for more details/examples. This value can be overriden with any JSON string, but should not be necessary.

Note: `USERS_TO_REMOVE` argument is not available because all deactivated users will be removed in Snowflake via separate airflow job.
</details>

### 🛑 Snowflake Stop

These jobs are defined in [`.gitlab-ci.yml`](https://gitlab.com/gitlab-data/analytics/-/blob/master/.gitlab-ci.yml).

#### `clone_stop`

Runs automatically when MR is merged or closed. Do not run manually.

## Data Test Pipelines

All the below run against the Prod DB using the changes provided in the repo. No cloning is needed to run the below.

#### `🧠 all_tests_prod`

Runs through all tests in the analytics & data tests repo.

#### `💾 data_tests_prod`

Runs through all the data tests in the analytics & data tests repo's.

#### `schema_tests_prod`

Runs through all the schema tests in the analytics & data tests repo's.

#### `specify_tests_prod`

Runs specified model tests with the variable `DBT_MODELS`
