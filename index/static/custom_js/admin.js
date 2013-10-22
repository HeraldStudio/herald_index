
OK_RESPONSE_STATUS = "success"
OK_OPERATE_RESPONOSE = "True"



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCsrfHeader()
{
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}



function setPubLinkClick()
{
    $("#pub_link").click(function(){
        data = {
            "link_name":$("#link_name").val(),
            "link_url":$("#link_url").val(),
            "link_level":$("#link_level").val()
        }
        setCsrfHeader();
        $.post("/index/admin/save_link/",data,function(rd, status){
            resetLink();
            alert(rd);

        });
        return false;
    });

}

function setResetLinkClick()
{
    $("#reset_link").click(function(){
        resetLink();
        return false;
    });
}

function resetLink()
{
    $("#link_name").val('');
    $("#link_url").val('');
    $("#link_level").val('0');
}


function setPubNewsClick()
{
    $("#pub_news").click(function(){
        alert("pub news click");
        data = {
            "title":$("#title").val(),
            "link":$("#link").val(),
            "headline":$("#headline").is(":checked")
        }
        alert($("#headline").is(":checked"));
        setCsrfHeader();
        $.post("/index/admin/save_news/", data, function(rd, status){
            resetNews();
            alert(rd);
        });
        return false;
    });
}

function setResetNewsClick()
{
    $("#reset_news").click(function(){
        resetNews();
        return false;
    });
}

function resetNews()
{
    $("#title").val("");
    $("#link").val("");
    $("#headline").attr("checked", false);
}

function setPubRecClick()
{
    $("#pub_rec").click(function(){
        pubRec();
        return false;
    });

}

function setResetRecClick()
{
    $("#reset_rec").click(function(){
        resetRec();
        return false;
    });
}

function resetRec()
{
    $("#rec_title").val("")
    $("#rec_link").val("")
    $("#rec_up_pic").val("")
    $("#rec_intro").val("")
}

function pubRec()
{
    setCsrfHeader();
    $.ajaxFileUpload
    (
        {
            url:'/index/admin/upload_rec_pic/',
            secureuri:false,
            fileElementId:'rec_up_pic',
            dataType: 'json',
            success: function (data, status)
            {
//                alert(data.picname + " "+status);
                pubRecText(data.picname);
            },
            error: function (data, status, e)
            {
                alert(e);
            }
        }
    )
}

function pubRecText(picname)
{
    data={
        "rec_title":$("#rec_title").val(),
        "rec_link":$("#rec_link").val(),
        "rec_intro":$("#rec_intro").val(),
        "rec_pic_name":picname
    }
    setCsrfHeader();
    $.post("/index/admin/save_recommend/", data, function(){
        resetRec();
        alert("publish recommend success!");
    });
}

function setPubWrapper()
{
    $("#pub_wrapper").click(function(){
    setCsrfHeader();
    $.ajaxFileUpload
    (
        {
            url:'/index/admin/upload_wrapper_pic/',
            secureuri:false,
            fileElementId:'wrapper_up_pic',
            dataType: 'json',
            success: function (data, status)
            {
//                alert(data.picname + " "+status);
                saveWrapperText(data.picname);
            },
            error: function (data, status, e)
            {
                alert(e);
            }
        }
    )

//        alert("pub wrapper");
        return false;
    });
}

function saveWrapperText(picname)
{
    data = {
        "title":$("#wrapper_name").val(),
        "intro":$("#wrapper_intro").val(),
        "tip":$("#wrapper_tip").val(),
        "tip_url":$("#wrapper_tip_url").val(),
        "img_name":picname
    }
    setCsrfHeader();
    $.post(
        "/index/admin/save_wrapper/",
        data,
        function(data, status){
            if (data=="True"&&status=="success")
            {
                alert("发布成功");
            }
            else
            {
                alert("发布失败");
            }
        }
    );
}


function setResetWrapper()
{
    $("#reset_wrapper").click(function(){
        $("#wrapper_name").val("");
        $("#wrapper_intro").val("");
        $("#wrapper_tip").val("");
        $("#wrapper_tip_url").val("");
        $("#wrapper_up_pic").val("");
        return false;
    });
}


function setWrapperNumClick()
{
    $("#set_wrapper_num").click(function(){
        num = $("#wrapper_num").val();
        setCsrfHeader();
        $.post(
            "/index/admin/set_wrapper_num/",
            {"wrapper_num":num},
            function(data, status){
                if(data=="True" && status=="success")
                {
                    alert("设置成功");
                }
                else
                {
                    alert("设置失败");
                }
            }
        );
        return false;
    });

}


function setPubAppClick()
{
    $("#pub_app").click(function(){
        setCsrfHeader();
        $.ajaxFileUpload
        (
            {
                url:'/index/admin/upload_app_pic/',
                secureuri:false,
                fileElementId:'app_up_pic',
                dataType: 'json',
                success: function (data, status)
                {
    //                alert(data.picname + " "+status);
                    saveAppText(data.picname);
                },
                error: function (data, status, e)
                {
                    alert(e);
                }
            }
        )
        return false;
    });
}

function saveAppText(imgname)
{
    data = {
        "name": $("#app_name").val(),
        "intro": $("#app_intro").val(),
        "url" : $("#app_link").val(),
        "img_name":imgname
    }
    setCsrfHeader();
    $.post(
        "/index/admin/save_app/",
        data,
        function(data, status){
            if (data==OK_OPERATE_RESPONOSE &&  status==OK_RESPONSE_STATUS)
            {
                alert("发布成功");
            }
            else
            {
                alert("发布失败");
            }
        }
    );
}


