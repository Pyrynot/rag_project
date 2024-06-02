---
title: "Data For Product Managers"
---

This page is intended to help Product Managers at GitLab understand what data is available to them and how they can use it to understand how their product is used. This page primarily covers two topics: _how_ to consume data, and _what_ data is available.

## How to Consume Data at GitLab

The user-facing end of GitLab's data stack is comprised of our BI Tool, Tableau which is connected to our Snowflake data warehouse. The [Tableau handbook page](/handbook/business-technology/data-team/platform/tableau/) of the data team handbook has general information about Tableau aimed for a wider GitLab audience.

#### Useful links for Product Managers

Here are some useful links that we recommend for you to bookmark:

- [Product Manager Toolkit](/handbook/business-technology/data-team/data-catalog/xmau-analysis/product-manager-toolkit.html)
- [Data Catalog](/handbook/business-technology/data-team/data-catalog)
- [DBT documentation](https://gitlab-data.gitlab.io/analytics/#!/overview) (where most of our models are documented)
- [Service Ping Metrics Dictionary](https://metrics.gitlab.com/)
- [Service Ping documentation](https://docs.gitlab.com/ee/development/service_ping/)
- [Snowplow documentation](https://docs.gitlab.com/ee/development/snowplow/)
- [Analytics Instrumentation Quick Links](https://about.gitlab.com/direction/analytics/analytics-instrumentation/#quick-links)
- [Product Data Insights handbook](/handbook/product/product-analysis/)

#### Getting Access

- Everybody at GitLab should automatically have view access granted through Okta.
- To create your own charts + dashboard, you'll need to have a Creator or Explorer license - you can read more about the Tableau license types [here](/handbook/business-technology/data-team/platform/tableau/#capabilities). Create an [access request](https://gitlab.com/gitlab-com/team-member-epics/access-requests/-/issues/new?issuable_template=New+Access+Request) asking for the appropriate license type. These access requests can be assigned to a data team manager.

#### The 2 basic building blocks in Tableau are charts and dashboards

- Charts are queries to the data warehouse, materialized into visualizations.
- Dashboards are collections of charts and have a unique URL (like a "page").
- If you have a Creator or Explorer license, you'll be able to create both of these.

#### How do I know what tables are available?

- The data team uses a tool called [dbt](https://www.getdbt.com/) for our data transformation layer. A nice feature of dbt is dbt docs, which automatically creates documentation for all of the models in our schema. Our dbt docs instance can be found [here](https://gitlab-data.gitlab.io/analytics/#!/overview).
    - Tableau will show a list of all tables available for querying when you form a connection to Snowflake in the Data Source pane.
    - ![''](/handbook/business-technology/data-team/programs/data-for-product-managers/schemas.png)
    - Table names are always prefixed by their source name. So the table that stores the ngroups table from the gitlab dotcom database is available at `legacy.gitlab_dotcom_groups`

##### How can I update or add more information to the dbt docs?

You will need to locate the file you wish to update or create in the [gitlab-data analytics project](https://gitlab.com/gitlab-data/analytics). Please be sure to read and follow the [SQL style guide](/handbook/business-technology/data-team/platform/sql-style-guide/) when creating the changes. If you wish to update only the descriptions or information about tables you will be looking for a `schema.yml` file. If you wish to actually change the structure of tables it will be a `*.sql` file.

Next, create a branch and then submit an MR using the `dbt Model Changes` template to the [gitlab-data analytics project](https://gitlab.com/gitlab-data/analytics). When creating your branch and MR please folow the [data team workflow](/handbook/business-technology/data-team/how-we-work/#merge-request-workflow) and use the appropriate [data team labels](/handbook/business-technology/data-team/how-we-work/#issue-labeling).

#### How does data get into the warehouse?

- Through a couple different ways which are detailed [here](/handbook/business-technology/data-team/platform/#extract-and-load).

#### How can I get help?

- If you ever get stuck or have a question, please ask for help in the #data slack channel and cross-post in your #g_, #s_, or #product channels. Many PMs have data related expertise and can provide you quick assistance for common product data questions.
- Remember, it's helpful for us to know the context behind your question. Don't just say _what_ you want to know but also _why_ so others can point you to a more efficient way to get your answer.
- This document is meant to serve as a guide of best practices. Please add what you learn when you need help to this content.
- As a last resort, you may create an issue in the [data team project](https://gitlab.com/gitlab-data/analytics/issues/new) with the Product label and assign it to a [product data analyst](/handbook/business-technology/data-team/#product). There are issue templates that are useful for specifying your request. The data team has limited bandwidth and is primarily focused on [improving self-serve capabilities](/handbook/business-technology/data-team/direction/self-service/). When creating issues please ping your [Section Leader](/handbook/product/product-leadership/#product-leaders) on the issue to ensure it is prioritized appropriately within the data team.

## Key Data Sources for Product Managers at GitLab

The first question we on the data team ask product managers is usually "are you interested in knowing this for self-managed or GitLab.com?" Our approach to answering your question differs greatly between the two. Although our self-managed offering has many more active customers, our GitLab.com offering has much more data available to analyze.

- We have three primary data sources that are useful from a product perspective.
    - **Service Ping** (for Self-Managed and GitLab.com)
    - **GitLab.com Postgres Database** (for GitLab.com)
    - **Snowplow** (for GitLab.com)

### Service Ping (Version App)

- [Service Ping](https://docs.gitlab.com/ee/administration/settings/usage_statistics.html) is a custom tool that GitLab built to deal with the problem of collecting weekly aggregate information from our customers who host our product on their own hardware.
- It is optional but defaults to being on.
- You can see the percent of paid subscriptions that successfully send a ping every month on [this chart](hhttps://10az.online.tableau.com/t/gitlab/views/DevelopmentPDCentralizedMetricsDashboard/MetricReporting/4c1649dc-2d4d-444d-9fc7-470d2ef21e58/9176da06-6f61-4e95-b3a7-14ae391cfc8f). We do not know about unlicensed (core) users but assume the same rate. Here is more [information](https://gitlab.com/gitlab-org/analytics-section/analytics-instrumentation/internal/-/issues/291#note_276741996) on why some instances block data from being sent.
- GitLab.com service pings can be filtered out of your query using the `ping_delivery_type` field.
- Monthly totals for Service Ping are added to Snowflake daily. By the 2nd all the data should be available from the previous month.

**Query Example filtering out GitLab.com:**

```sql
SELECT *
FROM common_mart.mart_ping_instance
WHERE ping_delivery_type != 'SaaS'
LIMIT 100
;
```

#### Snippets

Published data Tableau sources are great ways to allow Tableau users to build charts without writing any SQL or modeling. The data team has created several Published data Tableau sources that have the official badge. Any published data sources that are trusted data will have the [TD] prefix.

We created several snippets that allow you to get quickly without any SQL writing some feature usage from the Service Pings data source.
You can find details about those snippets on the [Product Manager Toolkit](/handbook/business-technology/data-team/data-catalog/xmau-analysis/product-manager-toolkit.html) handbook page.

### GitLab.com Postgres Database

- Because GitLab.com is a GitLab instance hosted by GitLab, we have access to the instance's postgres database and can load parts of it into our snowflake data warehouse. This means we can get a very detailed look into how our product is used on GitLab.com.
- This is largely an **untapped resource** as historically not many PMs have known that this data was consistently available in BI tools.
- Any part of the product that creates a table on the backend (see the [schema](https://gitlab.com/gitlab-org/gitlab/-/blob/master/db/structure.sql) file) can be added to the ELT job which will sync 3x a day to the warehouse. From there, all we need to do is build a dbt base model to make them accessible in Tableau.

#### What if the table or column I want isn't in the data warehouse?

- Our ELT process works by explicitly stating which columns and tables we want to import into the data warehouse. This means we might be missing a column or whole table that you want to have in the data warehouse for analysis.
- When this is the case, please create a data issue letting us know what you want us to import. Before doing so, please confirm that the table/column is truly part of the [production schema](https://gitlab.com/gitlab-org/gitlab/-/blob/master/db/structure.sql).

#### Replicating Service Ping using GitLab.com Data

- Because service ping only aggregates data at an `instance` level, it is not super useful for GitLab.com since we often want to see information at the `namespace` level. For example, knowing that 40K people used your stage on GitLab.com is somewhat useful, but you'll probably want to know more context (Are they free or paid? What plan are they on? Do I have any power users or is usage equally distributed?)
- But since we have access to the GitLab.com postgres database, we are capable of replicating any part of service ping at the namespace level or even the user level.
- All service ping does under the hood is execute some `SELECT COUNT(*) FROM x` statements, making it trivial to replicate.
- [This model](https://gitlab-data.gitlab.io/analytics/#!/model/model.gitlab_snowflake.mart_event_valid) exemplifies hows service ping could be replicated for GitLab.com at the namespace level. This model is available as a discovery dataset in Tableau.

#### Examples

### Snowplow

- Snowplow Analytics is an open-source enterprise event-level analytics platform that enables data collection from multiple platforms for advanced data legacy.
- GitLab.com currently uses two of these snowplow tracking libraries: JavaScript and Ruby.
    - With the JS library, we track a lot of front-end activity automatically (All page views, sessions, link clicks, some button clicks, etc.) We also utilize structured events to capture specific events with defined business logic.
- We do not track `user_id` on any of the snowplow events, making all events functionally anonymous. This severely limits the utility of these events.
- We have found the [Snowplow Inspector](https://chrome.google.com/webstore/detail/snowplow-inspector/maplkdomeamdlngconidoefjpogkmljm?hl=en) to be very useful in tracing and debugging events being sent through the browser.
- Snowplow is not sending data from self-managed instances. If they deem it helpful, the instance administrator can [configure their own Snowplow endpoint](https://docs.gitlab.com/ee/development/snowplow/#enable-snowplow-tracking) for the events.

#### What can Product Managers do?

A lot!

Because Snowplow doesn't rely on Service Ping and is mainly for GitLab SaaS, data from Snowplow is much faster to collect (as soon as the feature is deployed) and visualize.

As mentioned, even though the anonymization of snowplow events is a major limitation, with the fast feedback, it is an effective source of data to measure feature adoption and usage.

We recommend Product Managers and their teams use [Snowplow custom structured events](https://github.com/snowplow/snowplow/wiki/canonical-event-model#customstruct), which are Snowplow's canonical events. We have built [`Tracking`](https://docs.gitlab.com/ee/development/snowplow/implementation.html#snowplow-javascript-frontend-tracking) and [`GitLab::Tracking`](https://docs.gitlab.com/ee/development/snowplow/implementation.html#implement-ruby-backend-tracking), 2 wrappers for Snowplow JavaScript and Ruby Trackers respectively.

- JavaScript trackers can be used to collect users' frontend action, especially clicks.
- Ruby trackers can be used to collect any event happening in the backend. For example, we currently use them for monitor:APM. More information in this [issue](https://gitlab.com/gitlab-org/gitlab/issues/121724)

To get started, use the [Snowplow event tracking template](https://gitlab.com/gitlab-org/gitlab/-/blob/master/.gitlab/issue_templates/Snowplow%20event%20tracking.md) when [creating a new Snowplow tracking issue](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Snowplow%20event%20tracking)

#### Snowplow structured event taxonomy

Please read our [Snowplow Guide](https://docs.gitlab.com/ee/development/snowplow/index.html#structured-event-taxonomy) for more information around the recommended taxonomy.

#### Testing your events

Once your Snowplow events have been instrumented, as part of the validation process, the newly instrumented event should be tested to ensure they're working properly. While you as the PM probably won't be doing the validation yourself everytime, it is nice to know how it works. The content under this heading should help you get started.

Testing Snowplow events can be tricky. Snowplow doesn't have a proper testing interface. However, several tools can help you debug, test, and validate your events implementation:

- When working on your local instance: you can use [Snowplow Micro](https://snowplow.io/blog/introducing-snowplow-micro/). [This video is a nice tutorial on getting started with Snowplow Micro](https://www.youtube.com/watch?v=OX46fo_A0Ag).
- In the near future, we plan to implement [Snowplow Mini](https://github.com/snowplow/snowplow-mini) as a way to QA our events on our staging environment. You can follow the progress [in this issue](https://gitlab.com/gitlab-org/analytics-section/analytics-instrumentation/internal/-/issues/266).

#### Visualize your events in Tableau

The data you have instrumented is useful only if it can be visualized in a chart. Refer to the [Tableau section](/handbook/business-technology/data-team/platform/tableau/) of the handbook for information on creating charts.

- Check if they are correctly stored in Snowflake in the [Snowplow Event Exploration Dashboard](https://10az.online.tableau.com/#/site/gitlab/workbooks/2294309). You can use the filters to find your events. If you are not sure of the value of the different attributes, they should have been captured in your issue using [Snowplow event tracking template](https://gitlab.com/gitlab-org/gitlab/-/blob/master/.gitlab/issue_templates/Snowplow%20event%20tracking.md). If not, check with your engineering manager.
- Once you have verified that your events is properly stored. You are ready to query and visualize the data! Please be aware that we are collecting several millions of events (page views, structured events) per month, so the whole dataset is quite slow to query. In order to make  it easy to explore this data source we have created several smaller and more compact tables:
  - [`legacy.snowplow_structured_events_all`](https://gitlab-data.gitlab.io/analytics/#!/model/model.gitlab_snowflake.snowplow_structured_events_all): contains ALL structured events
  - [`legacy.snowplow_page_views_all`](https://gitlab-data.gitlab.io/analytics/#!/model/model.gitlab_snowflake.snowplow_page_views_all): contains ALL page views
  - [`legacy.snowplow_unstructured_events_all`](https://gitlab-data.gitlab.io/analytics/#!/model/model.gitlab_snowflake.snowplow_unstructured_events_all): contains ALL unstructured events (including click events, form submissions, etc).

{{% panel header="**PRO TIP: Optimizing queries**" header-bg="info" %}}
To make your query faster, use a date filter in your `WHERE` statement.

Example query:

```sql
SELECT
  event_action,
  COUNT(*) AS event_count
FROM legacy.snowplow_structured_events_all
WHERE  derived_tstamp > CURRENT_DATE-30
GROUP BY 1
ORDER BY 2 DESC
```

{{% /panel %}}

#### Some Issues and Merge Requests examples

TODO

### Other data sources\*\*

- **Sheetload**
- You can load your own Google Sheets into the data warehouse. Read more [here](/handbook/business-technology/data-team/platform/#using-sheetload).

## Analytics Instrumentation

- [Analytics Instrumentation](https://about.gitlab.com/direction/analytics/analytics-instrumentation/) is part of the product org and is completely separate from the Data team. However, the Data team and the Analytics Instrumentation collaborate closely as Product Analytics Fusion Team.
- The Analytics Instrumentation team members are the [DRI](/handbook/people-group/directly-responsible-individuals/)s for data collection across both GitLab.com and Self-Managed. They own Service Ping and Snowplow. They are the ones to go to for questions like:
    - How do I instrument a new statistic for self-managed?
    - What are the best practices for adding to service ping?
    - How can I use snowplow to track a frontend interaction on GitLab.com?
    - Can I utilize snowplow to track events on the server-side?
