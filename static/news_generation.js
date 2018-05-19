$("#year").change(showLevels);
$("#level").change(showLocations);
$("#location").change(showCycles);
$("#cycle").change(showFocus);
$("#focus").change(showFields);
$(".btn-reset").click(resetQuery);
$(".btn-generate").click(generateNews);
$(".news-delete").click(deleteNews);
$(".news-download").click(downloadNews);
function showLevels() {
	$("#level").val("")
	showLocations()
	if ($("#year").val() != null) {
		$('#level').find('option').remove().end().append('<option selected disabled>Pilih Tingkat..</option>')
		$.ajax({
            url: '/getLevel',
            data: {year: $("#year").val()},
            type: 'POST',
            success: function(response) {
                level = JSON.parse(response).level
                for (i = 0; i < level.length; i++) {
                	$('#level').append($("<option></option>").attr("value",level[i]).text(level[i])); 
                }
                $(".level").removeClass("hidden")
            },
            error: function(error) {
                console.log(error);
            }
        });
	}
	else {
		$(".level").addClass("hidden")
	}
}
function showLocations() {
	$("#location").val("")
	showCycles()
	if ($("#level").val() != null) {
		$('#location').find('option').remove().end().append('<option selected disabled value="">Pilih Daerah Pemilihan..</option>')
		$.ajax({
            url: '/getLocation',
            data: {year: $("#year").val(), level: $("#level").val()},
            type: 'POST',
            success: function(response) {
                loc = JSON.parse(response).loc
                for (i = 0; i < loc.length; i++) {
                	$('#location').append($("<option></option>").attr("value",loc[i]).text(loc[i])); 
                }
                $(".location").removeClass("hidden")
            },
            error: function(error) {
                console.log(error);
            }
        });
	}
	else {
		$(".location").addClass("hidden")
	}
}
function showCycles() {
	$("#cycle").val("")
	showFocus()
	if ($("#location").val() != null) {
		$('#cycle').find('option').remove().end().append('<option selected disabled value="">Pilih Putaran..</option>')
		$.ajax({
            url: '/getCycle',
            data: {year: $("#year").val(), level: $("#level").val(), location: $("#location").val()},
            type: 'POST',
            success: function(response) {
                cycle = JSON.parse(response).cycle
                for (i = 0; i < cycle.length; i++) {
                	$('#cycle').append($("<option></option>").attr("value",cycle[i]).text(cycle[i])); 
                }
                $(".cycle").removeClass("hidden")
            },
            error: function(error) {
                console.log(error);
            }
        });
	}
	else {
		$(".cycle").addClass("hidden")
	}
}
function showFocus() {
	$("#focus").val("")
	showFields()
	if ($("#cycle").val() != null) {
		$('#focus').find('option').remove().end().append('<option selected disabled value="">Pilih Fokus Berita..</option>')
		$.ajax({
            url: '/getFocus',
            data: {year: $("#year").val(), level: $("#level").val(), location: $("#location").val(), cycle: $("#cycle").val()},
            type: 'POST',
            success: function(response) {
                focus = JSON.parse(response).focus
                for (i = 0; i < focus.length; i++) {
                	$('#focus').append($("<option></option>").attr("value",focus[i]).text(focus[i])); 
                }
                $(".focus").removeClass("hidden")
            },
            error: function(error) {
                console.log(error);
            }
        });
	}
	else {
		$(".focus").addClass("hidden")
	}
}
function showFields() {
	$("#sublocation").val("")
	$("#entity").val("")
	$("#value_type").val("")
	if ($("#focus").val() != null) {
		$('#entity').find('option').remove().end().append('<option selected value="">All</option>')
		$('#sublocation').find('option').remove().end().append('<option selected disabled>Pilih Lokasi Pencoblosan..</option>')
		$('#value_type').find('input').remove()
		$('#value_type').find('label').remove()
		$.ajax({
            url: '/getFields',
            data: {year: $("#year").val(), level: $("#level").val(), location: $("#location").val(), cycle: $("#cycle").val(), focus: $("#focus").val()},
            type: 'POST',
            success: function(response) {
                sublocation = JSON.parse(response).sublocation
                for (i = 0; i < sublocation.length; i++) {
                	$('#sublocation').append($("<option></option>").attr("value",sublocation[i]).text(sublocation[i])); 
                }
                $(".sublocation").removeClass("hidden")
                value_type = JSON.parse(response).value_type
                for (i = 0; i < value_type.length; i++) {
                	$('#value_type').append("<div class='form-check'></div>").append($('<input></input>').attr({'type': 'checkbox', 'name':'value_type', 'value': value_type[i]}))
                 	$('#value_type').append("<label class='form-check-label' style='font-weight: normal'>  "+ value_type[i] +"</label>")
                }
                $(".value_type").removeClass("hidden")
                if ($("#focus").val() != "Pemilih") {
                	entity = JSON.parse(response).entity
                	$('#entity-label').text($("#focus").val());
	                for (i = 0; i < entity.length; i++) {
	                	$('#entity').append($("<option></option>").attr("value",entity[i]).text(entity[i])); 
	                }
	                $(".entity").removeClass("hidden")
                } else {
                	$(".entity").addClass("hidden")
                }

            },
            error: function(error) {
                console.log(error);
            }
        });
	}
	else {
		$(".entity").addClass("hidden")
		$(".sublocation").addClass("hidden")
		$(".value_type").addClass("hidden")
	}
}
function resetQuery(event) {
	event.preventDefault();
	swal({
		title: "Apakah Anda Yakin?",
		text: "Setelah dilakukan reset, query anda akan hilang",
		icon: "warning",
		buttons: true,
	    closeOnConfirm: true,
    	closeOnCancel: true,
		dangerMode: true,
	}).then((willDelete) => {
  		if (willDelete) {
    		swal("Query anda terhapus. Silahkan masukan query baru");
    		window.location = "http://127.0.0.1:5000/news_generation";
	 	} 
	});
}
function isAllFilled() {
	var isBlank = false
    $(".required").each(function() {
        if($(this).val() == null) {
            isBlank = true  
        }
    });
    if (isBlank) {
    	return false
    } else {
    	if ($("form input:checkbox:checked").length == 0) {
    		return false
    	}
    	else {
    		return true
    	}
    }
}
function generateNews(event) {
	event.preventDefault(); 
	$('.modal-body').find('p').remove()
	var a = isAllFilled()
	if (!a) {
		swal({
			icon: "error",
			title: "Query belum terisi",
			text: "Isi dahulu query yang dibutuhkan",
		});
	} else {
		formData = $("form").serialize()
		swal({
			icon: "warning",
			title: "Apakah Anda Yakin?",
			text: "Berita akan dibangkitkan sesuai dengan query anda",
			buttons: true,
		}).then((willGenerate) => {
	  		if (willGenerate) {
		        $.ajax({
		            url: "/generateNews",
		            type: "POST",
		            data: formData,
		            success: function (response) {
		   	        	article =  JSON.parse(response).article
		   	        	citytime = JSON.parse(response).citytime
		   	        	article = article.replace(/(?:\r\n|\r|\n)/g, '<br>');
		   	        	citytime = citytime.replace(/(?:\r\n|\r|\n)/g, '<br>');
		   	        	$('.modal-body').append("<p class='news' id='news'><b>"+ citytime + "</b>" + article +"</p>")
		                $('#modal-news').modal('show'); 
		            },
		            error: function (error) {
			        	swal({
				         	title: "Berita gagal dibangkitkan!",
				         	icon: "error",
				         });
		            	console.log(error)
		            }
		        });
		 	} 
		});
	}
}

function deleteNews(event) {
	event.preventDefault();
	swal({
		title: "Apakah Anda Yakin?",
		text: "Setelah ditutup, berita ini akan hilang jika belum disimpan",
		icon: "warning",
		buttons: true,
	    closeOnConfirm: true,
    	closeOnCancel: true,
		dangerMode: true,
	}).then((willDelete) => {
  		if (willDelete) {
    		swal("Berita Anda berhasil dihapus");
    		$('.modal-body').find('p').remove()
    		$('#modal-news').modal('hide');
	 	} 
	});
}
function downloadNews(event) {
	event.preventDefault();
	a = document.getElementById("news").innerText;
    $.ajax({
        url: "/downloadNews",
        type: "POST",
        data: {article: a},
        success: function (response) {
	         status = JSON.parse(response).status
	         if (status == "ok") {
	         	swal({
	         		title: "Berita berhasil disimpan!",
	         		icon: "success",
	         	});
	         } else {
	         	swal({
	         		title: "Berita gagal disimpan!",
	         		icon: "error"
	         	});
	         }
        },
        error: function (error) {
        	console.log(error)
        	swal({
	         	title: "Berita gagal disimpan!",
	         	icon: "error",
	         });
        }
    });
}