<!DOCTYPE html>
<html lang="es">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="icon" type="image/svg+xml" href="faviconconfiguroweb.png" />
	<title>Ejemplo ChatGPT</title>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.1/css/bootstrap.min.css" integrity="sha512-B3clz06N8Jv1N/4ER3q4ee4+AVa8rrv/5Q5M5tz+R5S9t8XvJyA2+7nFt2QdC8dPwZlnwyF+I1tKb/nik18Ovg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
	<script src="https://kit.fontawesome.com/a076d05399.js"></script>
</head>
<body>
<h1>BIENVENIDOS</h1>
    <!DOCTYPE html>
</body>
</html>

<html lang="es">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>login</title>
	<link rel="stylesheet" href="css/login.css">
	<link rel="stylesheet" href="css/cabecera.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.0.0/animate.min.css">
	
	<!-- Include necessary CSS and JS files -->
    <style>
        /* Chatbot container */
        .chatbot-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            width: 300px;
            font-size: 11px;
            color: #333;
            z-index: 9999;
            display: flex;
            flex-direction: column;	
			border-color: black;
        }

        /* Chat messages */
        .chat-messages {
            flex: 1;
            overflow-y: auto;
			overflow-x: auto;
			min-height: 0; /* Allow the container to shrink below its default height */
			max-height: 450px;
        }

        /* User message style */
        .user-message {
            color: black;
    		text-align: right;
        }

        /* Chatbot message style */
        .chatbot-message {
            color: green;
    		text-align: left;
			background-color: #DCDCDC;
        }

		/* Input form */
		.input-form {
			display: flex;
			margin-top: 0;
			margin-bottom: 0;
			padding: 0;
			border-radius: 0;
			width: 297px;
			background-color: #f1f1f1;	
    		margin-left: -9px;

		}

		/* User input field */
		.user-input {
    		margin-left: 0px;
			margin-top: 0px;
			background-color: #f1f1f1;
			width: 500px;	
			height: 30px;
            font-size: 11px;
    		text-align: left;		
		}

		/* Submit button */
		.submit-btn {
			background-color: #007bff;
			color: #fff;
			margin-top: 0;
			cursor: pointer;	
			height: 30px;
			width: 100px;
			margin-right: 1px;
		}

		/*.chatbot-container.auto-size {
		/*height: auto;
		max-height: 1500px; /* Set a maximum height to prevent the container from growing too large */
		/*overflow-y: auto;
		}*/		
    </style>
	
</head>
<body>
	<form action="validarCrearUsuario.php" method="post">
	<h1 class="animate__animated animate__backInLeft">Crear Usuario</h1>
	<input type="submit" value="Crear">
	</form> 

	<form action="validarCrearContacto.php" method="post">
	<h1 class="animate__animated animate__backInLeft">Crear Contacto</h1>
	<input type="submit" value="Crear">
	</form> 

	<form action="validarEditarUsuario.php" method="post">
	   <h1 class="animate__animated animate__backInRight">Editar Usuario</h1>
	   <input type="submit" value="Editar">
	</form>

	<form id="file-upload-form">
		<input type="file" id="file-input" name="file">
		<button type="button" id="upload-btn" class="btn btn-primary">Upload File</button>
	</form>
   
    <!-- Chat container -->
    <div class="chatbot-container">
        <div class="chat-messages" id="chat-messages"></div>
        <form class="input-form" id="chat-form">
            <input type="text" class="user-input" id="user-input" placeholder="Type your message here..." />
            <button type="submit" class="submit-btn">Send</button>
        </form>
    </div>
	
	<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
	
	<script>
		// Function to send user input to the server for processing
		function sendMessageToChatbot(userInput) {
			$.ajax({
			type: 'POST',
			url: 'chatbot.php',
			data: { message: userInput },
			success: function (response) {
				// Display the chatbot's response
				$('#chat-messages').append('<p class="chatbot-message"><strong>Chatbot:</strong> ' + response + '</p>');

				// Auto-scroll to the bottom of the container
				var container = document.getElementById("chat-messages");
				container.scrollTop = container.scrollHeight;
			},
			error: function (xhr, status, error) {
				// Handle the error if the server-side script encounters an issue
				console.error("Error processing user input:", error);
			},
			});
		}

		$(document).ready(function () {
			$('#chat-form').submit(function (event) {
			event.preventDefault();

			// Get user input
			var userInput = $('#user-input').val();

			// Clear the input field
			$('#user-input').val('');

			// Display user message in the chat
			$('#chat-messages').append('<p class="user-message"><strong>You:</strong> ' + userInput + '</p>');

			// Send user input to the server for processing with chatbot.php
			sendMessageToChatbot(userInput);
			});
		});
	</script>

	<script>
		$(document).ready(function () {
			// Handle file upload button click
			$('#upload-btn').click(function () {
				// Get the selected file
				var fileInput = document.getElementById('file-input');
				var file = fileInput.files[0];

				// Create a FormData object to send the file to the server
				var formData = new FormData();
				formData.append('file', file);

				// Send the file to the server using AJAX
				$.ajax({
					type: 'POST',
					url: 'file_upload.php', // Replace 'save_file.php' with the server-side script that handles the file upload and saving
					data: formData,
					processData: false,
					contentType: false,
					success: function (response) {
						// Display a success message to the user
						alert('File uploaded successfully!');
					},
					error: function () {
						// Display an error message to the user
						alert('File upload failed!');
					}
				});
			});
		});
	</script>

	<!-- Add this script at the end of your body tag -->
	<script>
		// Function to check if the code has been modified
		function isCodeModified() {
			// Modify the version number if you change the code
			var currentVersion = "1.0";
			var lastVersion = localStorage.getItem("codeVersion");
			
			// Check if the code has been modified or not
			if (lastVersion !== currentVersion) {
			// Set the current version as the last version in the localStorage
			localStorage.setItem("codeVersion", currentVersion);
			return true;
			}

			return false;
		}

		function runPythonScript() {
			$.ajax({
			type: "GET",
			url: "run_script.php", // Replace with the URL of the server-side script that executes the Python code
			success: function (response) {
				// Handle the response from the server if needed
				console.log("Python script executed successfully:", response);
			},
			error: function (xhr, status, error) {
				// Handle the error if the server-side script encounters an issue
				console.error("Error executing Python script:", error);
			},
			});
		}

		$(document).ready(function () {
			// Check if the code has been modified
			var codeModified = isCodeModified();

			if (codeModified) {
			// Call the function to run the Python script only on the first visit after code modification
			runPythonScript();
			}

			// Schedule the function to run every 8 hours (8 hours * 60 minutes * 60 seconds * 1000 milliseconds)
			//setInterval(runPythonScript, 8 * 60 * 60 * 1000);
			setInterval(runPythonScript, 2 * 60 * 1000);
		});
	</script>

	<script src="run_script.js"></script>
	
</body>
</html>
