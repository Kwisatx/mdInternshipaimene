<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Upload form</title>
    </head>

    <body>
		<form action="{{postMethod}}" method="post" enctype="multipart/form-data">
			please upload here the poi file <br>
			<input type="file" name="poi" /> <br>
			please umplad here the visit file <br>
			<input type="file" name="visits"/> <br> 
			<input type="submit" value="Submit"> 
		</form>
    </body>
</html>
