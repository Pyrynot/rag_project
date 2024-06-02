---

title: "Data Team Organization"
description: "GitLab Data Team Organization"
---









---

## Data Team Organization

The Data Team Organization model is guided by three primary business needs:

1. The need for **bespoke data solutions** unique to the GitLab business.
1. The need for **high-performance and reliable data storage and compute** platform to support distributed analyst teams.
1. The need for centers of excellence for **data technologies** and **advanced analytics**.
1. The need for flexible data solutions driven by varying **urgency and quality** requirements.

Based on these needs, the Data Team is organized in the following way:

1. **Data Pods:** Pods are assembled to provide concentrated focus on delivering & maintaining **data products** for **strategic company initiatives**. Pods are staffed with multiple data personas including Data Analyst, Data Scientist, Analytics Engineer, and supported by Data Engineer as stable counterpart.
1. **[Analytics Engineering](handbook/business-technology/data-team/#analytics-engineering-team):** Transform raw data into clean, structured, and usable formats for data decision-making. The Lead Analytics Engineer serves as a stable counterpart for business departments and functional analytics teams.
1. **[Data Platform & Engineering Team](/handbook/business-technology/data-team/#the-data-platform--engineering-team):** **Center of Excellence** for data technologies, including owning and operating the Data Stack
1. **[Data Science Team](/handbook/business-technology/data-team/#the-data-science-team):** **Center of Excellence** for advanced analytics, including delivery of data science projects to the business

## Data Pod Assignments

| POD                       | Data Product Manager | Analytics Engineer                     | Data Analyst    | Data Scientist |
| ------------------------- | -------------------- | -------------------------------------- | --------------- | -------------- |
| Enterprise Metrics        |  @nmcavinue          | @lisvinueza @chrissharp                | @annie-analyst  |                |
| Customer Intelligence     |  @nmcavinue          | @snalamaru                             | @jonglee1218      |                |
| Customer Product Adoption |  @mdrussell             | @michellecooper @utkarsh060 |                 |                |

## Analytics Engineering - Business Stable Counterpart Assignments

| Department       | Functional Analytics Team         | Analytics Engineer      |
| ---------------- | --------------------------------- | ----------------------- |
| Sales            |  Revenue Strategy and Analytics   |  @snalamaru             |
| Marketing        |  Marketing Strategy and Analytics |  @snalamaru             |
| Finance          |  FP&A Analytics                   |  @chrissharp            |
| Customer Success |  CS Strategy and Analytics        |  @mdrussell             |
| Product          |  Product Data Insights            |  @michellecooper             |
| Engineering      |  Engineering Analytics            |  @michellecooper        |
| Security         |  Engineering Analytics            |  @michellecooper        |
| Support          |  N/A                              |  @michellecooper        |
| People           |  People Analytics                 |  @rakhireddy (ramping)  |

## Data Platform Team Stable Counterpart Assignments

| POD | Data Engineer |
| --- | ------------- |
| Enterprise Metrics | @juwong |
| Customer Intelligence | @rigerta |
| Customer Product Adoption | @rbacovic |

### Manager, Data

In support of the Data Pod, the Manager, Data fulfills the below responsibilities from the [Senior Manager, Data](/job-families/finance/manager-data/#senior-manager-data) Job Responsibilites:

1. Works with the Director, Data to envision and draft Quarterly Objectives, driven by requirements gathered from multiple business partners.
1. Monitor, measure, and improve key aspects of the Data Pods.
1. Regularly meet with business partners to understand and solve for data needs.
1. Serve as a primary or back-up Maintainer on the Data Team Project. Provide final review, feedback, and approval of Merge Requests submitted by the Data Pod and stable counterparts.

### Lead Analytics Engineer (Stable Counterparts for the Business)

In support of the Data Pod and Stable Counterpart relationships, the Lead Analytics Engineer fulfills the below responsibilities from the [Senior Analytics Engineer](/job-families/finance/analytics-engineer/#senior-analytics-engineer-responsibilities) Job Responsibilites:

1. Own one or more stakeholder relationship in Go To Market, Research & Development, General & Administrative, Financial Analytics, or Engineering Analytics business functions.
1. Co-DRI of Key Results along with the Manager, Data.
1. Lead [work breakdown](/handbook/business-technology/data-team/how-we-work/planning/#work-breakdowns) sessions for OKRs.
1. Work with functional stakeholders to prioritze `P3-Other` issues.
1. Serve as a primary or back-up Maintainer on the Data Team Project. Provide final review, feedback, and approval of Merge Requests submitted by the Data Pod and stable counterparts.
1. Review the weekly stand-up and provide support as needed to unblock team members and answer questions.

### Data Platform Team Stable Counterpart

Following the GitLab [Stable Counterpart](/handbook/leadership/#stable-counterparts) principles, every **Data Pod** have a **Data Platform Team** Stable Counterpart assigned. The Data Platform Stable Counterpart divides their time, work and priorities between the Data Platform Team and Data Pod (general an average of 50% each, P2-OKR scheduled ahead of the quarter in collaboration with the respective Pod). The Stable Counterpart is aware of the direction and priorities of the Data Pod and when needed brought into discussion with the Data Platform Team. I.e. when there is a bigger demand than the Stable Counterpart can handle in the assigned availability or architectural direction needs to change. The Stable Counterpart recognize, flags and address this with the applicable stakeholders (in general the Lead/DRI of the Data Platform Team and the Data Pod).

The stable counterpart is expected to participate in the following meetings asynchronously or synchronously. When in doubt, please reach out to the Data Pod Manager to learn which meetings on the calendar you should participate in. In general, the meetings in scope are as follows:

1. Data Pod Iteration Planning Meetings.
1. Data Pod Team Meetings.

## Data Program Recruiting

Recruiting great people is critical to our success and we've invested much effort into making the process efficient. Here are some reference materials we use:

- a [GitLab Data Recruiting](https://youtu.be/4DlwsBIPxUw) video to say "Hi" and give you some insight into how we work and what we work on. Enjoy!
- [Data Roles and Career Development](/handbook/business-technology/data-team/organization/#data-roles-and-career-development) to help existing team members and prospects understand growth opportunities
- a [Take Home Test](/handbook/business-technology/data-team/organization/#data-roles-and-career-development) that we ask each candidate to complete; this test is good for the candidate and for us because it represents the type of work we perform regularly and if the candidate is not interested in this work it helps them make a more informed decision about their application

## Data Roles and Career Development

## Data Internships

See [Data Team Internships](/handbook/business-technology/data-team/organization/internships/).

## Data Platform

- [Data Engineering Job Family](/job-families/finance/data-engineer)

```mermaid
  graph LR;
  subgraph Data Engineering Roles
    supe:de(Data Engineer)-->supe:sde(Senior Data Engineer);
    supe:sde(Senior Data Engineer)-->supe:fde(Staff Data Engineer);
  end

  click supe:de "https://handbook.gitlab.com/job-families/finance/data-engineer#data-engineer";
  click supe:sde "https://handbook.gitlab.com/job-families/finance/data-engineer#senior-data-engineer";
  click supe:fde "https://handbook.gitlab.com/job-families/finance/data-management#staff-data-engineer";
```

### Intermediate and Senior Data Engineer Onboarding Timeline

| By Day 30 | By Day 60 |  By Day 90 | By Day 120 |
| ------ | ------ |------ |------ |
| Complete People and Data Onboarding | Perform [triage](/handbook/business-technology/data-team/how-we-work/triage/) activities | Extract [new data sources](/handbook/business-technology/data-team/how-we-work/new-data-source/) | Own a specific area of the data platform |
| Create a MR to contribute to handbook or templates | Investigate incidents and issues | Work on [OKR assignments](/handbook/business-technology/data-team/direction/#quarterly-objectives) | Propose new ideas and come up with Data Platform improvement initiatives |
| Understand the current setup of the data platform | Make small/corrective changes to the platform infrastructure or data pipelines | Contribute on work breakdown | |

## Data Analyst

- [Data Analyst Job Family](/job-families/finance/data-analyst)

```mermaid
  graph LR;
  subgraph Data Analyst Roles
    supe:ida(Data Analyst Intern)-->supe:jda(Junior Data Analyst);
    supe:jda(Junior Data Analyst)-->supe:da(Data Analyst);
    supe:da(Data Analyst)-->supe:sda(Senior Data Analyst);
    supe:sda(Senior Data Analyst)-->supe:fda(Staff Data Analyst);
  end

  click supe:ida "https://handbook.gitlab.com/job-families/finance/data-analyst#data-analyst-intern";
  click supe:jda "https://handbook.gitlab.com/job-families/finance/data-analyst#junior-data-analyst";
  click supe:da "https://handbook.gitlab.com/job-families/finance/data-analyst#data-analyst";
  click supe:sda "https://handbook.gitlab.com/job-families/finance/data-analyst#senior-data-analyst";
  click supe:fda "https://handbook.gitlab.com/job-families/finance/data-analyst#staff-data-analyst";
```

### Intermediate and Senior Data Analyst Onboarding Timeline

| By Day 30 | By Day 60 |  By Day 90 | By Day 120 |
| ------ | ------ |------ |------ |
| Complete People and Data Onboarding | Extend an existing Tableau dashboard or complete the triage phase for a dbt issue | Run a project end-to-end as DRI with support from a Data Fusion Team | Create ERDs/Data Artifacts (e.g. dashboards) or complete a product evaluation|
| Start attending [Data Fusion Team](/handbook/business-technology/data-team/#data-fusion-teams) and Business Team synchronous meetings | Perform [triage](/handbook/business-technology/data-team/how-we-work/triage/) activities | | |
| Complete First Issue: S to M T-Shirt Size  |  |  |  |

## Data Science

- [Data Science Job Family](/job-families/finance/data-science)

```mermaid
  graph LR;
  subgraph Data Science Roles
    supe:ds(Data Scientist)-->supe:sds(Senior Data Scientist)-->supe:stds(Staff Data Scientist)-->supe:pds(Principal Data Scientist);
  end

  click supe:ds "https://handbook.gitlab.com/job-families/finance/data-science/#data-scientist-intermediate";
  click supe:sds "https://handbook.gitlab.com/job-families/finance/data-science/#senior-data-scientist";
  click supe:stds "https://handbook.gitlab.com/job-families/finance/data-science/#staff-data-scientist";
  click supe:pds "https://handbook.gitlab.com/job-families/finance/data-science/#principal-data-scientist";
```

### Intermediate and Senior Data Scientist Onboarding Timeline

| By Day 30 | By Day 60 |  By Day 90 | By Day 120 |
| ------ | ------ |------ |------ |
| Complete People and Data Onboarding | Meet stakeholders across the organization | Re-train or enhance an existing data science model |  Make a contribution to improve the Data Science handbook, packages, or processes |
| Start attending Data Science Team meetings | Refine/improve one data science dashboard | Work on [OKR assignments](/handbook/business-technology/data-team/direction/#quarterly-objectives) | Take ownership of at least one quarterly OKR |
| Understand the current data science systems and processes |  | |  |

## Analytics Engineering

### [Analytics Engineering Job Family](/job-families/finance/analytics-engineer)

```mermaid
  graph LR;
  subgraph Analytics Engineer Roles
    supe:ae(Analytics Engineer)-->supe:sae(Senior Analytics Engineer);
    supe:sae(Senior Analytics Engineer)-->supe:fae(Staff Analytics Engineer);
    supe:fae(Staff Analytics Engineer)-->supe:pae(Principal Analytics Engineer);
  end

  click supe:ae "https://handbook.gitlab.com/job-families/finance/analytics-engineer#analytics-engineer-intermediate";
  click supe:sae "https://handbook.gitlab.com/job-families/finance/analytics-engineer#senior-analytics-engineer";
  click supe:fae "https://handbook.gitlab.com/job-families/finance/analytics-engineer#staff-analytics-engineer";
  click supe:pae "https://handbook.gitlab.com/job-families/finance/analytics-engineer#principal-analytics-engineer";
```

### Intermediate and Senior Analytics Engineer Onboarding Timeline

| By Day 30 | By Day 60 |  By Day 90 | By Day 120 |
| ------ | ------ |------ |------ |
| Complete People and Data Onboarding  | Extend an existing dbt [Trusted Data Models](/handbook/business-technology/data-team/data-development/#trusted-data-development) | Run a project end-to-end as DRI with support from a Data Fusion Team | Create ERDs/Data Artifacts|
| Start attending Data Fusion Team and Business Team synchronous meetings | Perform [triage](/handbook/business-technology/data-team/how-we-work/triage/) activities | | |
| Complete First Issue: S to M T-Shirt Size  |  |  |  |

## Data Management

- [Data Management Job Family](/job-families/finance/manager-data)

```mermaid
  graph LR;
  subgraph Data Management Roles
    supe:md(Manager, Data)-->supe:smd(Senior Manager, Data);
    supe:smd(Senior Manager, Data)-->supe:dd(Director, Data);
    supe:dd(Director, Data)-->supe:sdd(Senior Director, Data);
  end

  click supe:md "https://handbook.gitlab.com/job-families/finance/manager-data/#manager-data-intermediate";
  click supe:smd "https://handbook.gitlab.com/job-families/finance/manager-data/#senior-manager-data";
  click supe:dd "https://handbook.gitlab.com/job-families/finance/data-and-insights-executive/#director-data-and-analytics";
  click supe:sdd "https://handbook.gitlab.com/job-families/finance/data-and-insights-executive/#senior-director-data-and-analytics";
```

### Data Manager Onboarding Timeline

| By Day 30 | By Day 60 |  By Day 90 | By Day 120 |
| ------ | ------ |------ |------ |
| Complete People, Data, and Manager Onboarding | Meet everyone on the team and business data champions | Complete a Team Assessment | Draft a people development Roadmap |
| Understand the current setup of the data platform | Work on [OKR assignments](/handbook/business-technology/data-team/direction/#quarterly-objectives) and map them to the data platform | Lead discussions with Users/Stakeholders on initiatives and OKRs | Draft a program development Roadmap (Process Improvements /Future State) |
| Add a new page to the handbook | Make regular contributions to the handbook spanning your area of management | Become DRI for major portions of the Data Handbook | System/Application Change Control Management of one or more modules |
