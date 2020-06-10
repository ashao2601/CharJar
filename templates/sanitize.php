<?php

function prepareInput($inputData){
	$inputData = trim($inputData);
	$inputData = htmlspecialchars($inputData);
	return $inputData;
}

?>
