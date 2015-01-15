/* Javascript for {{ class-id }} card */

$('#i-info-{{ class-id }}').click(function()
{
	/* icons */
	$('#i-info-{{ class-id }}').css('display','none');
	$('#i-close-{{ class-id }}').show();
	$('#i-{{ class-id }}').show();
	
	/* content */
	$('#accordion-{{ class-id }}').css('display','none');
	$('#desc-{{ class-id }}').show();

	/* color */
	$('#card-{{ class-id }}').css('background','#bbd4de');	
});


$('#i-close-{{ class-id }}').click(function()
{
	/* icons */
	$('#i-info-{{ class-id }}').show();
	$('#i-close-{{ class-id }}').css('display','none');
	$('#i-{{ class-id }}').css('display','none');
	
	/* content */
	$('#accordion-{{ class-id }}').show();
	$('#desc-{{ class-id }}').css('display','none');

	/* color */
	$('#card-{{ class-id }}').css('background','#e4eef2');	

});