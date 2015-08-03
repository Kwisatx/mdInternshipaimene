<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Mobility Traces Upload Form</title>
    </head>

    <body>
		<form action="{{postMethod}}" method="post" enctype="multipart/form-data"> 
			please upload here the mobility traces csv file <br>
			<input type="file" name="traces" /> <br> 
			<input type="submit" value="Submit"> 
		</form>
    </body>
</html>
