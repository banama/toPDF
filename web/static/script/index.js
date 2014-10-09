define(function(require, exports) {
    require('jquery')
    
    $('#submit').click(function(){
        var pdfcode = $('#pdfcode').val()
        $('.loading').css('display', '');
        $.post('/exsit', {'pdfcode': pdfcode}, function(data){
            if (data === "t"){
                $('.loading').html("<a href=" + pdfcode + '.pdf'
                    + "><img src='static/image/pdf.png' width='128px' height='128px'>");
                $('.refer').css('display', '');
                var refers = "<p>在你的网页引用下载该文件</p>" + "<pre>" +
"&lt;a href='http://topdfs-pdf.stor.sinaapp.com/" +  pdfcode + 
".pdf'&gt;&lt;img style='position: fixed; top: 75px; right: 75px; border: 0;'" + 
"src='static/image/pdf32.png'&gt;&lt;/a&gt;"
                $('.refer').html(refers);
            }
            else{
                $('.loading').css('display', 'none');
            }
        })
    })
});