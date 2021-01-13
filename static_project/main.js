
$(document).ready(function(){
	$('.list-unstyled').hide()
	let display = false
	$(".cform").submit(function(e){
		e.preventDefault();

		form = $(this)
		url = form.attr('action')
		text = form.find('input[name="text"]').val(),
		post_id = form.find('input[name="post_id"]').val(),
		csrf = form.find('input[name="csrfmiddlewaretoken"]').val(),
		 fd = new FormData()
		fd.append('csrfmiddlewaretoken',csrf)
		fd.append('text', text)
		fd.append('post_id', post_id)
		

		$.ajax({
			type : 'POST',
			url : url,
			enctype : 'multipart/form-data',
			data : fd,
			success : function(response){
				var s = "<li><p><a href="+response.url+"><strong>"+response.name+"</strong></a>"+response.text+"</p></li>"
				$('#'+post_id).append(s)
				form.find('input[name="text"]').val('')
				span = $('.span-'+post_id)
				count = parseInt(span.text())
				span.text(count+1)
				// $('.span-'+post_id).text(count+1)
			},
			processData : false,
			contentType : false,
		})

	})

	$('.like_form').submit(function(e){
			e.preventDefault();
			form = $(this)
			url = form.attr('action')
			x = form.find('button[name=btn]').val()
			post_id = form.find('input[name=p_id]').val()
			csrf = form.find('input[name=csrfmiddlewaretoken]').val()

			fd = new FormData()
			fd.append('csrfmiddlewaretoken',csrf)
			fd.append('post_id',post_id)

			$.ajax({
				type : 'POST',
				url  :url,
				enctype : 'multipart/form-data',
				data : fd,
				processData : false,
				contentType : false,
				success : function(response){
					btn = form.find('button')
					btn.toggleClass('bg-transparent')
					btn.toggleClass('btn-primary')
					id = form.find('button').attr('id')
					x = btn.text()
					if (id == 'like'){
						x = parseInt(x)-1
						btn.text(" "+x) 
						btn.attr('id','unlike')
						}
					else{
						x = parseInt(x)+1
						btn.text(" "+x) 
						btn.attr('id','like')
						}
					}
				})
		})

	$('.btn-light').click(function(){
		if (display == false) {
			$(this).next('.list-unstyled').show()
			display = true
		}
		else{
		$(this).next('.list-unstyled').hide()
			display = false	
		}
		
	})


})
