# 29.05

Models are trained on a specific set of data, and they have a knowledge cutoff date, so often they don't know specifics.

RAG, which stands for Retrieval, Augmentation, and Generation, can be quite helpful addressing this problem by inserting likely relevant, up-to-date text as context during inference time to go along with the question/instruction. It does this by storing the relevant documents in a vector database, and during inference time, querying it to find similar texts.

There are a lot of open-source libraries for this, which I'll probably be using, since this is only a 5-credit course. However, building my own framework could be an extremely rewarding experience, that no doubt would teach me a lot, and I could continue using and refining it for my personal projects. I might begin with building my own, and if that proves too challenging, switch to a library.

From the last project I learned that good planning is an important part of any project.

Possible datasets I could try RAG on:

- Old School Runescape Wiki
- KAMK Intra articles (english ones)
- O'Reilly's textbooks
- GitLab Handbook (https://gitlab.com/gitlab-com/content-sites/handbook)

The handbook repo includes the entire GitLab handbook in .md files, and it's all formatted nicely.
This could be a good subset to start: https://gitlab.com/gitlab-com/content-sites/handbook/-/tree/main/content/handbook/business-technology/data-team?ref_type=heads

It's the handbook section of the Data team.
