<?php

	mysql_connect('localhost', 'root', 'toor');
	mysql_select_db('test');

	$plus = isset($_GET['id']) ? '`id` = \''.$_GET['id'].'\'' : '1';
	$query = 'SELECT `id`, `info` FROM info WHERE '.$plus;

	$q = mysql_query($query);

	if(!mysql_num_rows($q))
	{
		echo 'Sorry, no result...';
		exit;
	}

	while(list($id, $info) = mysql_fetch_array($q))
	{
		echo '<a href="?id='.$id.'">Info #'.$id.'</a> : '.$info.'<br />';
	}
