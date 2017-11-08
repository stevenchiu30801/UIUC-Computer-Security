<meta charset="utf-8">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

<html>
<body>

%if type == 'GET':
    <h1>A GET request was sent</h1>
%else:
    <h1>A POST request was sent</h1>
%end

<br>
<br>

<p>The following parameters were sent:</p>

Name: {{name}} 
<br>
COB: {{cob}}

%if ssn:
	<p>The SSN for this user is: {{ssn}}
%else:
	<p>There is no user with the passed in credentials
%end

</body>
</html>