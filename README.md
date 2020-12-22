<h1>Utility Scripts</h1>

<div>
<p>This package contains modules with classes and functions to simplify app development.</p>
</div>

<div>Modules
  <ul>
    <li><code>dash_tools.py</code> objects for Dash app development.</li>
    <li><code>dbase.py</code> objects for working with MongoDB and OBIEE.</li>
    <li><code>email.py</code> objects for sending SMTP emails.</li>
    <li><code>fsconn.py</code> objects for fileserver connections.</li>
    <li><code>log.py</code> objects for logging operations.</li>
  </ul>
<p>See <code>setup.py</code> for packing and installing steps.</p>
</div>
<hr>

<div>
<h3>Optional Environment Variable Support</h3>
<p>Suggested use of environment variables is using a <code>.env</code> file. See 
<a href="https://pypi.org/project/python-dotenv/">python-dotenv</a> on <a href="pypi.org">pypi.org</a> for more info. 
See module documentation for a list of built-in environment variables.</p>
</div>
<hr>

<div>
<h3>To Run Unit Tests</h3>
<p>Run the following command from the <code>/utility_scripts_package</code> directory (substitute <code>python</code> 
for <code>python3</code> on windows).</p>
<p><code>python3 -m unittest discover -v tests</code></p>
</div>
<hr>
