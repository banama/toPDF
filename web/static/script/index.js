define(function(require, exports) {
    require('jquery')
    
    $('#submit').click(function(){
        var pdfcode = $('#pdfcode').val()

        $('.refer').css('display', 'none');
        $('.nopdf').css('display', 'none');
        $('.loading').css('display', '');
        $('.pdf').html('')

        $.post('/exsit', {'pdfcode': pdfcode}, function(data){
            if (data === "t"){
                $('.loading').css('display', 'none');
                $('.pdf').css('display', '');
                $('.pdf').html("<a href='http://topdfs-pdf.stor.sinaapp.com/" + pdfcode + '.pdf'
                    + "'><img src='http://topdfs-pdf.stor.sinaapp.com/pdf.png' width='128px' height='128px'>");
                
                $('.refer').css('display', '');
                var refers = "<p>在你的网页引用下载该文件</p>" + "<pre>" +
"&lt;a href='http://topdfs.sinaapp.com/pdf/" +  pdfcode + 
"' target='_blank' &gt;&lt;img style='position: fixed; top: 75px; right: 75px; border: 0;'" + 
"src='http://download.easyicon.net/png/1168993/32/'&gt;&lt;/a&gt;"
                $('.refer').html(refers);
            }
            else{
                $('.loading').css('display', 'none');
                $('.nopdf').css('display', '');
                $('.refer').css('display', 'none');
            }
        })
    })
});