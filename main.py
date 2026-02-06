from agent import build_email_agent


email_text = """
Subject: Meeting reschedule

Hi,

Can we move tomorrow's 2pm meeting to next Monday morning?

Also please share the latest project status before the meeting.

Thanks!
"""


agent = build_email_agent()


task = f"""
You are an AI email assistant.

1) Classify the email.
2) Extract TODO items.
3) Write a short polite reply.
4) Save draft with:
   to="client@example.com"
   subject="Re: Meeting reschedule"

Email:
{email_text}
"""


result = agent.run(task)

print("AGENT RESULT:")
print(result)
