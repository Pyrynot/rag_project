---

title: "SAFE Data Guide"
description: "SAFE Data Guide"
---









---

## What is SAFE Data?

The Data Team follows the GitLab SAFE [Framework](/handbook/legal/safe-framework/) when it comes to SAFE Data. Sometimes also `MNPI` and `RESTRICTED_SAFE` is used in relation to SAFE Data and the SAFE Framework.

## Access to SAFE Data

### Tableau

Access to Tableau dashboards is based on license type (see Tableau Licenses in our [Tableau](/handbook/business-technology/data-team/platform/tableau/) handbook page), which can be prioritized by job roles, and governed by the [SAFE Data Access Framework](/handbook/legal/safe-framework/). In Tableau, we apply the SAFE security framework using [User Groups](/handbook/business-technology/data-team/platform/tableau/#user-groups). There are four primary projects/folders where dashboards can exist - Development, Production, Ad-hoc, and Resources. The Development, Production, and Ad-hoc folders each have a sub-folder for various teams at GitLab, such as Finance and Sales. Within each team's folder there are generally two main folders to which content can be published: General, and SAFE.

- The General folders contain data that can be viewed by anyone at GitLab.
- The SAFE folders contain any dashboards with material non-public information (MNPI) and are only accessible by users belonging to the General SAFE Access user group.

The development workflow for Tableau Creators that work with data meeting [GitLab's SAFE criteria](/handbook/legal/safe-framework/#safe-flowchart) is to publish into the SAFE folder in their department's Development project. Should the Creator want to publish the workbook outside of the SAFE folder within the development project, they should open an [issue](https://gitlab.com/gitlab-data/tableau/-/issues/new) using the `All Requests` template in the Tableau project and request a review of the content by the BI Platform team. The BI Platform team will provide a yes or no decision on whether it is SAFE to publish the content outside of the SAFE folder in the development project.

#### Accessing a GitLab General Access Dashboard

General Access Dashboards are available to all GitLab Team members. An Access Request to gain access to Tableau (if a team member does not already have access) will be required, but no further Access Requests are required to view these general access dashboards. You can read more about permissions and access in the [Tableau Section](/handbook/business-technology/data-team/platform/tableau/#permissions) of the handbook.

#### Accessing a SAFE Dashboard

All SAFE dashboards are stored within various team's SAFE folders and permission is managed by the user's access group membership. Access to a single SAFE dashboard provides access to all SAFE Dashboards. Having  access to the SAFE project/folder will result in making the team member a [Designated Insider](/handbook/legal/publiccompanyresources/#sts=Designated%20Insiders) subject to our [Insider Trading Policy](https://drive.google.com/file/d/12H-H43vIf15fWADZDEf3FH2jneMmiLDH/view). Gaining access to a SAFE dashboard (and the space) via membership in the General SAFE Access user group requires:

1. Your immediate manager's approval
2. Departmental VP (or equivalent) approval

To gain access to SAFE dashboards:

1. Create an [Access Request](https://gitlab.com/gitlab-com/team-member-epics/access-requests/-/issues/24284) for Tableau - SAFE Access - [Requestor Name].
2. Request approval from your immediate manager and your Departmental VP (or equivalent). Approval is needed if it concerns a new Access Request(/issue).
3. Once the request is approved, follow the instructions in the tech_stack.yml file for provisioning.
4. After processing is complete you will be able to log in to Tableau and access your requested SAFE dashboard and all other dashboards which require SAFE access.

Please see the [Accessing](/handbook/business-technology/data-team/platform/#warehouse-access) SAFE Data in Snowflake for instructions on to access the SAFE data in Snowflake.

SAFE Data in Google Sheets files can be accessed using the instructions for [Accessing a SAFE Dashboard](/handbook/business-technology/data-team/platform/safe-data/#accessing-a-safe-dashboard). Please follow those instructions to gain access to SAFE Data in Google Sheets.

##### Deprovisioning SAFE Dashboard access

Every 90 days the Data Team runs a [Data Health and Security Audit](/handbook/business-technology/data-team/data-management/). In this audit the Data Team also checks for inactive usage. In case a GitLab Team Member hasn't used the SAFE Dashboard space for more than 90 days, access will be deprovisioned. To get access again to the SAFE Dashboard space, a new AR needs to be created and all approvals need to be obtained again.

#### Accessing Various Limited Access User Groups

There are several variations of limited access user groups which you may want to access, such as internal audit-related data, or sales development SAFE data. You can read about the descriptions of these groups [here](/handbook/business-technology/data-team/platform/tableau/#limited-access-user-groups), as well as how to request access.

### Snowflake

All SAFE Data are stored in tables and views within separate database schemas in Snowflake. Access to 1 table provides access to all SAFE tables. Access to SAFE data requires:

1. Your immediate manager's approval.
2. Departmental VP (or equivalent) approval.

To gain access to SAFE Data:

1. Create an [Access Request](https://gitlab.com/gitlab-com\team-member-epics/access-requests/-/issues\new?issuable_template=Individual_Bulk_Access_Request) and provide your needs and intent.
2. Request approval from your immediate manager and your Departmental VP (or equivalent). Approval is needed if it concerns a new Access Request(/issue).
3. Once the request is approved, tag the Snowflake [provisioners](https://gitlab.com/gitlab-com/www-gitlab-com/-/blob/master/data/tech_stack.yml) and they will process the request.
4. After processing is complete you will be able to access SAFE Data (schemas) in Snowflake.

## Data Development

SAFE Data in Snowflake is stored in separate schemas. Schemas with SAFE Data are prefixed with: `RESTRICTED_SAFE_*`. All models that contain MNPI data must be stored in these schemas. There is a [CI-Pipeline](/handbook/business-technology/data-team/platform/ci-jobs/#safe_model_script) (`safe_model_script`) that secures this process. Every model that is created or changed, will be checked by the CI-Pipeline. As a developer, the following governance needs to be taken into account:

- `mnpi` tag to be applied when reading out of a table/model that holds MNPI data and MNPI is used in the model. Subsequently the data must be stored in a `RESTRICTED_SAFE_*` schema.
- `mnpi_exception` tag to be applied when reading out of a table/model that holds MNPI data and MNPI is **not** used in the model. I.e. only a NON-MNPI field is used from a MNPI model.
- It's up to the engineer to determine if and which tag needs to be applied. Check the data that is exposed in your model against the GitLab SAFE [Framework](/handbook/legal/safe-framework/). If there is doubt, reach out in the. `#SAFE` channel in Slack.
- The CI pipeline is there to help and check fact based (upstream model tags versus current model tags).

The following diagram describes the process in detail when handling or referencing SAFE Data.

![MR Process](mnpi_dbt_models.png)
