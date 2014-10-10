define(function(require, exports) {
    require('jquery')
    
    $('#submit').click(function(){
        var pdfcode = $('#pdfcode').val()

        $('#save').css('display', 'none');
        $('.refer').css('display', 'none');
        $('.nopdf').css('display', 'none');
        $('.loading').css('display', '');
        $('.pdf').html('')

        $.post('/exsit', {'pdfcode': pdfcode}, function(data){
            if (data === "t"){
                $('.loading').css('display', 'none');
                $('.pdf').css('display', '');

                $('.pdf').html("<a href='http://topdfs-pdf.stor.sinaapp.com/" + pdfcode + ".pdf'" + " value='" + pdfcode
                    + "'><img src='http://topdfs-pdf.stor.sinaapp.com/pdf.png' width='128px' height='128px'></a>"
                    );
                
                $('.refer').css('display', '');
                var refers = "<p>在你的网页引用下载该文件</p>" + "<pre>" +
"&lt;a href='http://topdfs.sinaapp.com/pdf/" +  pdfcode + 
"' target='_blank' &gt;&lt;img style='position: fixed; top: 75px; right: 75px; border: 0;'" + 
"src='http://topdf.qiniudn.com/pdf32.png'&gt;&lt;/a&gt;"
                $('.refer').html(refers);
                $('#save').css('display', '');
            }
            else{
                $('.loading').css('display', 'none');
                $('.nopdf').css('display', '');
                $('.refer').css('display', 'none');
            }
        })
        


         $('#save').click(function(){
            $.post('/save', {'pdfmark':pdfcode}, function(data){
                if (data === 't'){
                    window.location.reload()
                }
                else{
                    alert('false');
                }
            })
        })
    })
});