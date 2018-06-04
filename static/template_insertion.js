$(".btn-fill-submit").click(insertOneTemplate);

function insertOneTemplate(event) {
	event.preventDefault();
	var a = isAllFilled();
	if (!a) {
		swal({
			icon: "error",
			title: "Template dan Kondisi belum terisi",
			text: "Isi dahulu template dan kondisi yang dibutuhkan",
		});
	} else {
		var submission = $(".form-fill-template").serialize()
		swal({
			icon: "warning",
			title: "Apakah Anda Yakin?",
			text: "Template akan dimasukkan sesuai dengan masukan anda",
			buttons: true,
		}).then((insertTemplate) => {
	  		if (insertTemplate) {
		        $.ajax({
		            url: "/insertTemplate",
		            type: "POST",
		            data: submission,
		            success: function (response) {
			         	status = JSON.parse(response).status
				         if (status == "ok") {
				         	swal({
				         		title: "Template berhasil disimpan!",
				         		icon: "success",
				         	});
				         } else {
				         	swal({
				         		title: "Template gagal disimpan!",
				         		icon: "error",
				         	});
				         }
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

function isAllFilled() {
	var isBlank = false
    $(".required").each(function() {
        if($(this).val() == null || $(this).val() == "") {
            isBlank = true  
        }
    });
    if (isBlank) {
    	return false
    } else {
    	return true
    }
}