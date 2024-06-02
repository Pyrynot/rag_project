---

title: "Data Development"
description: "This page defines the Data Development lifecycle"
---








## Data Development at GitLab

GitLab deploys two distinct but interrelated approaches to build data solutions that help drive insights and business decisions. These approaches are complementary to one another and are focused on delivering results at a level of speed, quality, and reliability required by the business, problem being solved, and question being asked. The approaches are complementary and evolutionary in nature, enabling development in an earlier stage to be leveraged in a later stage if required. Data solutions developed at an early stage can be improved and enhanced to a later stage if there is sufficient business need to do so. All analysis follows the well-established [Data Analysis Process](/handbook/business-technology/data-team/organization/analytics/#data-analysis-process).

The two approaches are `Ad-Hoc` and `Trusted Data`. `Ad-hoc` development is done in the `WORKSPACE` schemas in Snowflake and in the `Ad-hoc` folders in Tableau. `Trusted Data` development is done in the `COMMON` and `SPECIFIC` schemas in Snowflake and in the `Trusted Data` folders in Tableau.

|             |  Ad-hoc |  Trusted Data |
| :--         |     :-: |           :-: |
| When To Use | **Prototyping / Directional / Urgent Analysis** | **Mission Critical Analysis / Operational Analysis**  |
| Manual adding data | optional | N/A |
| Creating own data structures | optional |  N/A |
| Visualization using [Tableau](/handbook/business-technology/data-team/platform/tableau/) | optional | **required** |
| Built Using the [Enterprise Dimensional Model](/handbook/business-technology/data-team/platform/edw) | optional | optional |
| Built Using Data from the `COMMON` or `SPECIFIC` schemas | optional | **required** |
| Registered in the [Data Catalog](/handbook/business-technology/data-team/data-catalog/) | N/A | **required** |
| Follows [Trusted Data Development](/handbook/business-technology/data-team/data-development/#trusted-data-development) process | N/A | **required** |
| Tested using the [Trusted Data Framework](/handbook/business-technology/data-team/platform/#tdf) | N/A | **required** |
| Auditable w/linkage to source systems | N/A | **required** |
| `Trusted Data Branded` |  N/A | **required** |

### Ad-hoc Data Development

**Ad-hoc** delivers a report or dashboard for one-time or limited use and it can also deliver a prototype, first iteration of a data solution that is not mature enough for a long-term, Trusted Data Solution yet. Ad-hoc development is performed when no existing data solution answers the questions being asked. Code developed for ad-hoc analysis for one-time or limited use is not written to be leveraged in a long-term solution; rather, it is a means to deliver results quickly. Code developed for ad-hoc analysis for prototypes and first iterations of data solutions can be leveraged in a long-term, Trusted Data Solution.

To complete ad-hoc analysis, Analysts typically write and run SQL queries against the Enterprise Data Warehouse and extract data to analyze using tools like Sisense or Python. Analysts and Analytics Engineers can also complete Ad-Hoc analysis using dbt and prototyping data solutions that can be leveraged in long-term, Trusted Data Solutions. At times, new data may need to be sourced from text files, spreadsheets, or other data sources. In many cases, the ad-hoc report solves for the immediate business need and no further action is required. However, sometimes the results of ad-hoc analysis yield results that require additional data modeling or dashboard development. In these cases, a more robust and trustworthy solution can be developed using Trusted Data Development.

Ad-hoc development gives ultimate flexibility to prototype data solutions. If a new data set needs to be explored and new transformations need to be built in a fast-paced, iterative way, the Ad-hoc Data Development approach can be used. Because of its flexible nature, not all ad-hoc data development is suitable to make mission critical decisions. It is often a first step for maturing the data solution. Care and caution should be taken when using ad-hoc data solutions to inform business making decisions.

Ad-hoc development is done either in the `WORKSPACE` OR `EXPLORATIONAL` schemas. The main difference between the two schemas is the permissions set. In the `WORKSPACE` schema, users do not have create/insert/update/drop permissions on Snowflake and must follow standard data team processes using dbt to update tables in the data warehouse. In the `EXPLORATIONAL` schema, users have create/insert/update/drop permissions on the schema. The permissions in the `EXPLORATIONAL` schema are non-standard and would be available to a smaller audience for ad-hoc work.

### Trusted Data Development

**Trusted Data** delivers the most complete, reliable, and accurate analytics available to an enterprise. Over time as an organization matures and value of analytics increases, Trusted Data evolves and development rigor also evolves, but the core steps remain consistent and include requirements gathering, design, iterative wireframing, testing, and operational monitoring. Trusted data solutions differ from ad-hoc reports because they include quality validations such as data testing, code review, and registration in the Data Catalog. Trusted data solutions can be built either in the Enterprise Dimensional Model (EDM) located in the `COMMON` schemas or in the `SPECIFIC` schema that models application data. Both solutions are trusted due to having data testing, code review, and registration in the Data Catalog.

The EDM `COMMON` solution is suitable to model business processes that are cross-application and cross-functional in nature such as the Order to Cash and Release to Adoption business processes. In those cases, the Kimball methodology allows us to join data together and develop a robust and easy to use star schema for analysis. The `SPECIFIC` application data solution is suitable for business processes that are not cross-application and cross-functional in nature such as the NetSuite data source. Overtime, a data model in the `SPECIFIC` schema could mature and require a dimensional model in the `COMMON` schema for cross-functional and cross-application purposes; however, the data in both schemas is trusted.

![data team development_process](data_team_development_process.png)

#### Trusted Data Solution Criteria

All Trusted Data solutions must meet the following criteria:

1. The business problem is defined with clear revenue impact established
1. A [Data project](https://gitlab.com/gitlab-data/analytics/-/issues) Epic is created to manage development
1. Requirements and success criteria are captured and tracked in the Epic
1. Scope is defined for v1.0 and v1.1, with a release cycle established up-front (e.g. weekly, bi-weekly, monthly)
1. A Dashboard Wireframe is created in Lucid or Sisense and shared with users, iterating to "final draft"
1. If a Dimensional Data Model solution is indicated, then the Dimensional Data Model is designed and integrated into the [Enterprise Dimensional Model Bus Matrix](https://docs.google.com/spreadsheets/d/1j3lHKR29AT1dH_jWeqEwjeO81RAXUfXauIfbZbX_2ME/edit#gid=742713121). This step is not applicable for data modeled in the `SPECIFIC` application schema.
1. (`DRAFT: Under review with Monte Carlo Project`) [Trusted Data Tests](/handbook/business-technology/data-team/platform/dbt-guide/#trusted-data-framework) are created and deployed
1. The solution enters a User Acceptance Testing phase, including data validations to source systems
1. The solution is registered in the [Data Catalog](/handbook/business-technology/data-team/data-catalog/)
1. The solution is deployed, including any required training and user enablement

## Database Implementation

In both **Ad-hoc** and **Trusted Data** development, data is made available in the `PROD` database, via multiple schemas. Data can be read out of multiple schemas in Snowflake and Sisense.

### Ad-Hoc Database Implementation

To make data available for **Ad-Hoc Data Development**, data is transformed and made available in the Snowflake `PROD` database. This data is available in two different schemas, `WORKSPACE` AND `EXPLORATIONAL`.

The `WORKSPACE` schemas for **Ad-Hoc Data Development** are prefixed with `WORKSPACE_` or `RESTRICTED_SAFE_WORKSPACE_` if it contains MNPI data. In order to make data available in the `PROD` database schemas, `dbt` models are created.

The `EXPLORATIONAL` schemas for **Ad-Hoc Data Development** are prefixed with `EXPLORATIONAL_` or `RESTRICTED_SAFE_EXPLORATIONAL_` if it contains MNPI data. In the schemas, users have read and write permissions in order to create tables, add columns and prototype data solutions. The schemas are setup up on departmental level and access is not provisioned on a lower grain than schema level. Functional ownership of the schemas resides with the departmental VP (or equivalent). This means that the VP needs to provide approval in case of an Access Request and carries the responsibility of proper usage of the data in the schema (i.e. in case of MNPI, PII and sensitive data). `EXPLORATIONAL` schemas are the least governed data schemas, which gives ultimate flexibility. Advise to use these schemas on a need-to-use base.

### Trusted Data Database Implementation

**Trusted data** is only available on the `PROD` database. It follows the EDM methodology or the Specific application methodology. There are dedicated schemas available in the `PROD` database for **Trusted data**. The schemas for **Trusted Data Development** are prefixed with `COMMON_` or `SPECIFIC`; or prefixed with `RESTRICTED_SAFE_COMMON_` or `RESTRICTED_SAFE_SPECIFIC` if it contains MNPI data. In order to make data available in the `PROD` database schemas, `dbt` models are created for transforming the data towards an Enterprise Data Model (fact and dimension tables) or Specific application tables.
