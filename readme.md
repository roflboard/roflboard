# roflboard

This textboard web app was developed by GPT-4, which is a massive rofl.

Setup:

`
    python3 -m pip install -r requirements.txt
`

Run:

`
    uvicorn main:app --reload --host 0.0.0.0
`

Create posts and replies by sending requests and using Swagger UI at `/docs`.


Prompts used:

1. Write a simple textboard web application using FastAPI. In this textboard you can post text posts and reply to them.
2. Now make a function that returns all posts, which has offset and limit options.
3. Now make the posts being saved in a SQLite database, use SQLAlchemy.
4. Now make index endpoint render all posts with replies.
5. Write html snippet that has a text form and button that sends POST request with `{"content": <form text>}` json to `/post/` endpoint.
7. Now update the page when user presses "Send" button.
8. Add similar form for each post that sends replies.
9. HTML hide form and make it appear when user presses "Reply" button.
