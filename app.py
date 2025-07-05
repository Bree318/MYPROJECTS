from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML for the input form
form_html = """
<!doctype html>
<title>Dark Humor Mad Libs</title>
<h1>🕯️ Dark Humor Mad Libs: The Haunted Job Interview 🕯️</h1>
<form method="post">
  {% for field in fields %}
    <label>{{loop.index}}. {{field}}</label><br>
    <input name="input{{loop.index}}" required><br><br>
  {% endfor %}
  <input type="submit" value="Create Story">
</form>
"""

# HTML for the story
story_html = """
<!doctype html>
<title>Your Dark Story</title>
<h1>😈 Your Dark Humor Story 😈</h1>
<p>
So there I was, wearing my most <strong>{{inputs[0]}}</strong> suit, holding a <strong>{{inputs[1]}}</strong>, and wondering why the receptionist just <strong>{{inputs[2]}}</strong> when I walked in.
</p>
<p>
The room was freezing, and I swear something brushed against my <strong>{{inputs[3]}}</strong>. Before I could scream, a <strong>{{inputs[4]}}</strong> fell from the ceiling with a <em>thud</em>.
</p>
<p>
"Welcome," said the <strong>{{inputs[5]}}</strong>, his voice like <strong>{{inputs[12]}}</strong> on a chalkboard. "You're our <strong>{{inputs[6]}}</strong>th applicant today. The others... didn’t make it."
</p>
<p>
I felt a wave of <strong>{{inputs[7]}}</strong>, but I stayed calm. I needed this job. Even if the interview room smelled like a <strong>{{inputs[1]}}</strong>'s rotting cousin.
</p>
<p>
"First question," he hissed. "Would you be willing to fight a <strong>{{inputs[8]}}</strong> for minimum wage?"
</p>
<p>
"Sure," I lied, wiping blood off my resume.
</p>
<p>
He smiled. "Excellent. One last thing: how do you feel about <strong>{{inputs[9]}}</strong> while <strong>{{inputs[10]}}</strong>?" He leaned closer and whispered, "We do have occasional issues with <strong>{{inputs[13]}}</strong>."
</p>
<p>
I glanced nervously at the wall of <strong>{{inputs[11]}}</strong>. "Completely fine."
</p>
<p>
He stood up. "You're hired."
</p>
<p>
And that’s how I got my dream job… and lost my <strong>{{inputs[3]}}</strong> on day one.
</p>
<p>
My name is <strong>{{inputs[14]}}</strong>. I used to be alive.
</p>
"""

@app.route("/", methods=["GET", "POST"])
def madlibs():
    fields = [
        "Adjective",
        "Noun",
        "Verb (past tense)",
        "Body part",
        "Type of weapon",
        "Job title",
        "Number",
        "Emotion",
        "Type of creature",
        "A horrible way to die",
        "Verb ending in -ing",
        "Plural noun",
        "Sound",
        "A very specific phobia",
        "Name"
    ]
    if request.method == "POST":
        inputs = [request.form.get(f"input{i+1}") for i in range(len(fields))]
        return render_template_string(story_html, inputs=inputs)
    return render_template_string(form_html, fields=fields)

if __name__ == "__main__":
    app.run(debug=True)
