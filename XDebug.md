Follow the below guide for installing the Visual Studio Code extension "PHP Debug"
https://stackify.com/php-debugging-guide/

Create a test site in XAMPP and create a index.php file with the below code
```php
<?php
	phpinfo();
	/*
	xdebug_info();
	
	function step_over_me() {
		echo 'stepping over me<br>';
	}
	
	function step_into_me() {
		step_over_me();
	}
	
	for ($i=0; $i < 100; $i++) {
		step_into_me();
	}
	*/
?>
```

CTRL-A the HTML on the test site and copy it to the XDebug Wizard Page
https://xdebug.org/wizard

Copy the DLL file to the proper location

Edit the php.ini file and paste the following at the bottom
```ini
    output_buffering = Off
    ; set the extension path
    zend_extension = "C:\xampp\php\ext\php_xdebug-3.0.1-7.3-vc15-x86_64.dll"
    ; allow remote debugging
    [XDebug]
    xdebug.remote_enable = 1
    xdebug.remote_autostart = 1
    # This should match your xdebug.remote_host
    xdebug.client_host=localhost
    # This should match your xdebug.remote_port
    xdebug.client_port=9000
    xdebug.mode=debug
```
