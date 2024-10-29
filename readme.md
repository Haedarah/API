<h1>Python APIs - Demo</h1>

<h2>Overview:</h2>

<p>In this project, we have a sample company (<strong>Company1</strong>) with a loyalty-points database (an excel sheet) and an API on top of it. We also have a platform (<strong>MONET</strong>) that provides two CLIs:<br>
A CLI that companies (e.g. Company1) use to get on-boarded on MONET, and a CLI that MONET itself uses for interacting with an on-board company.</p>

<p>Note: You may find in-detail technical documentation inside the scripts themselves.</p>

<h2>How to set up:</h2>

<h3>1. Company:</h3>
<p>In this part, we are setting up the sample company. After completing the below steps, you will have a running API on top of the company's database.</p>
<ol>
    <li>
        Head to <strong>COMPANY</strong> directory.
    </li>
    <li>
        <p>It is a good practice to <i>reset the database</i> before starting the API. To do so, run the following command:<br>
        <code>python restore_original_database.py</code></p>
    </li>
    <li>
        <p>Run the following command to <i>start the API</i>:<br>
        <code>python api.py</code><br>
        Keep the API running on the terminal, and open a new terminal to use in the next steps.</p>
    </li>
</ol>

<h3>2. MONET:</h3>
<p> After setting up the company, it is time to on-board it and interact with its API. Please follow the below steps to achieve that:</p>
<ol>
    <li>
        Head to <strong>MONET</strong> directory.
    </li>
    <li>
        <p>To on-board a company, run the following command:<br>
        <code>python onboarding.py</code><br>
        and fill the details of the company's API.</p>
    </li>
    <li>
        <p>Run the following command to <i>start the interaction CLI</i> and follow the instructions there:<br>
        <code>python querying.py</code></p>
    </li>
</ol>

