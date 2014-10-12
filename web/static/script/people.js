define(function(require, exports) {
    require('jquery')
                

    $.get('/pdflist', function(data){
        var datas = $.parseJSON(data);
        var htmls = $('.pdflist').html()
        for (var i = datas['pdflist'].length - 1; i >= 0; i--) {
            if(datas['pdflist'][i][0] == ''){
                htmls += '<li value="'+ datas['pdflist'][i][1] +'"><a href="http://topdfs-pdf.stor.sinaapp.com/' + datas['pdflist'][i][1] + 
                        '.pdf"><span><img src="http://topdf.qiniudn.com/pdf32.png"><span>' + 
                        datas['pdflist'][i][1] + '</a><a style="position:relative;right:0px;" class="remark" href="javascript:void(0);"> 备注</a>' +
                        '<span class="glyphicon glyphicon-remove remove" style="top:2px;" href="javascript:void(0);"></span></li>'
            }
            else{
                htmls += '<li value="'+ datas['pdflist'][i][1] +'"><a href="http://topdfs-pdf.stor.sinaapp.com/' + datas['pdflist'][i][1] + 
                        '.pdf"><span><img src="http://topdf.qiniudn.com/pdf32.png"><span>' + 
                        datas['pdflist'][i][0] + '</a><a style="position:relative;right:0px;" class="remark" href="javascript:void(0);"> 备注</a>' +
                        '<span class="glyphicon glyphicon-remove remove" style="top:2px;" href="javascript:void(0);"></span></li>'
            }
            $('.pdflist').html(htmls);
            console.log(datas['pdflist'][i][0])
            remark();
            removes();
        };
    });
    
    function remark(){
        $('.remark').click(function(){
            var origin = $(this).prev('a').text()
            var father = $(this).parent()
            var pdfmark = father.attr('value')
            var htmls = '<span><img src="http://topdf.qiniudn.com/pdf32.png"></span><input class="remark" value="'+ origin +'">' +
                    '</a><a style="position:relative;right:0px;" class="saveremark" href="javascript:void(0);"> 保存</a>'
            father.html(htmls)
            saveremark();
        });
    }

    function removes(){
        $('.remove').click(function(){
            var pdfmark = $(this).parent().attr('value')
            $.post('/delete', {'pdfmark' :pdfmark}, function(data){
                if (data === 't'){
                    window.location.reload()
                }
                else{
                    alert('false');
                    window.location.reload()
                }
            })

        })
    }

    function saveremark(){
        $('.saveremark').click(function(){
            var father = $(this).parent()
            var remarks = father.children('input').val()
            var pdfmark = father.attr('value')
            $.post('/remark', {'remarks': remarks, 'pdfmark': pdfmark}, function(data){
                if (data === 't'){
                    window.location.reload()
                }
                else{
                    alert('false');
                    window.location.reload()
                }
            })
        })

    }


    
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
                    + "'><img src='http://topdf.qiniudn.com/pdf.png' width='128px' height='128px'></a>"
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