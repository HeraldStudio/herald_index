/**
 * Created with PyCharm.
 * User: wolf
 * Date: 13-10-20
 * Time: 上午10:46
 * To change this template use File | Settings | File Templates.
 */

CURR_NEWS_PAGE = 1
CURR_REC_PAGE = 1
HAVE_MORE_NEWS = false

CURR_NEWS_MOD_ID = -1
CURR_REC_MOD_ID = -1
CURR_LINK_MOD_ID = -1

//$(".btn_del").click(function(){
//    postDeleteRequest();
//});

function deleteNews(obj)
{
    postDeleteRequest(obj);
}

function postDeleteRequest(obj)
{
    setCsrfHeader();
    $.post(
        "/index/admin/delete_news/",
        {"id":$(obj).parent().parent().attr("id")},
        function(data,status){
            if(data=="True" && status=="success")
            {
                alert("delete news success");
            }
            else{
                alert("delete news failed");
            }
        }
    );
}

//$(".btn_mod").click(function(){
//    CURR_NEWS_MOD_ID = $(this).parent().parent().attr("id")
//    initModePop();
//    $("#modify_news_modal").modal('show');
//});

function modify_news(obj)
{
    CURR_NEWS_MOD_ID = $(obj).parent().parent().attr("id")
    initModePop();
    $("#modify_news_modal").modal('show');
}

function initModePop()
{
    $("#news_pop_title").val($("tr#"+CURR_NEWS_MOD_ID).find("a")[0].text);
    $("#news_pop_link").val($("tr#"+CURR_NEWS_MOD_ID).find("a")[0].href);
    if($("tr#"+CURR_NEWS_MOD_ID).children().eq(1).text()=='True')
    {
         $("#news_pop_headline").attr("checked",true);
    }
    else
    {
        $("#news_pop_headline").attr("checked",false);
    }

}

$("#news_pop_pub_news").click(function(){

    setCsrfHeader();
    $("#modify_news_modal").modal('hide');
    data = {
        "id":CURR_NEWS_MOD_ID,
        "title":$("#news_pop_title").val(),
        "url":$("#news_pop_link").val(),
        "headline":$("#news_pop_headline").is(":checked")
    }
    $.post(
        "/index/admin/update_news/",
        data,
        function(d, status){
            if(status=="success")
            {
                alert("更改成功");
            }
            else
            {
                alert("更改失败");
            }
        });
});


function setNewsNextPage()
{
    $("#news_next_page").click(function(){
        refreshNewsList(1);
        return false;
    });
}

function refreshNewsList(relative_page)
{
    $.get("/index/admin/async_news/",
            {"page_num":CURR_NEWS_PAGE+relative_page },
            function(data, status){
                news_html = "";
                jsonArr = eval("("+data+")");
                if(jsonArr.length)
                {
                    CURR_NEWS_PAGE = CURR_NEWS_PAGE + relative_page;
//                    alert(jsonArr.length);
                    for(var i=0; i<jsonArr.length; ++i)
                    {
                        news = jsonArr[i];
                        news_html+=
                            ("<tr id='"+ news.id +"'>"+
                            "<td><span><a href='"+ news.url +"'>"+ news.title +"</a></span></td>"+
                            "<td class='hide'>"+ news.is_headline +"</td>"+
                            "<td><span>"+ news.date +"</span></td>"+
                            "<td><button class='btn btn-mini btn-warning btn_mod' onclick='modify_news(this);' >修改</button></td>"+
                            "<td><button class='btn btn-mini btn-danger btn_del' onclick='deleteNews(this);' >删除</button></td>"+
                            "</tr>");
                    }
                    $("#news_tbody").html(news_html);
                }
                else
                {
                    alert("没有更多了");
                }

            }
        );
}

function setNewsPrePage()
{
    $("#news_pre_page").click(function(){
        if( CURR_NEWS_PAGE <= 1)
        {
            alert("已经是第一页了");
        }
        else
        {
//            CURR_NEWS_PAGE = CURR_NEWS_PAGE - 1;
//            alert(CURR_NEWS_PAGE);
            refreshNewsList(-1);
        }

        return false;
    });
}


function deleteRec(obj)
{
    setCsrfHeader();
    id = $(obj).parent().parent().attr("id");
    $.post(
        "/index/admin/delete_recommend/",
        {"id":id },
        function(data, status){
            if(status == "success" && data=="True")
            {
                alert("delete recommendation successfully");
            }
            else
            {
                alert("failed to delete recommendation");
            }
        }
    );
    return false;
}

function modify_rec(obj)
{
    CURR_NEWS_MOD_ID = $(obj).parent().siblings(".rec_id").eq(0).text();
    initRecModal(obj);

    $("#modify_rec_modal").modal("show");
}

function initRecModal(obj)
{
    title = $(obj).parent().siblings().find("a")[0].text;
    link = $(obj).parent().siblings().find("a")[0].href;
    intro = $(obj).parent().siblings().eq(2).text();

    $("#rec_pop_title").val(title);
    $("#rec_pop_link").val(link);
    $("#rec_pop_intro").val(intro);
}

function postRecMod(img_path)
{
    setCsrfHeader();
    data = {
        "id":CURR_NEWS_MOD_ID,
        "title":$("#rec_pop_title").val(),
        "url":$("#rec_pop_link").val(),
        "intro":$("#rec_pop_intro").val(),
        "img_path":img_path
    }
    $.post(
        "/index/admin/update_rec/",
        data,
        function(data, status){
            if (data == "True" && status == "success")
            {
                alert("modify recommendation successfully!!");
            }
            else
            {
                alert("failed to modify recommendation");
            }

        }
    );
    return false;
}


$("#pop_pub_rec").click(function(){

    setCsrfHeader();
    $("#modify_rec_modal").modal("hide");
    $.ajaxFileUpload
    (
        {
            url:'/index/admin/upload_rec_pic/',
            secureuri:false,
            fileElementId:'rec_pop_up_pic',
            dataType: 'json',
            success: function (data, status)
            {
//                alert(data.picname + " "+status);

                postRecMod(data.picname);
            },
            error: function (data, status, e)
            {
                alert(e);
            }
        }
    )
    return false;

});

function setRecNextPage()
{
    $("#rec_next_page").click(function(){
        refreshRecModal(1);
        return false;
    });

}

function setRecPrePage()
{
    $("#rec_pre_page").click(function(){
        if(CURR_REC_PAGE>1)
        {
            refreshRecModal(-1);
        }
        else
        {
            alert("已经是第一页了！");
        }

        return false;
    });


}

function refreshRecModal(relative_page)
{
    $.get(
        "/index/admin/async_rec/",
        {"page_num":CURR_REC_PAGE+relative_page},
        function(data, status){
            if(status == "success")
            {
                jsonArr = eval("("+data+")");
                html = ""
                if(jsonArr.length)
                {
                    CURR_REC_PAGE += relative_page;
                    for(var i=0;i<jsonArr.length;++i)
                    {
                        rec = jsonArr[i];
                        html += (
                            "<tr id='"+ rec.id +"'>"+
                                "<td><span><a href='"+ rec.url +"'>"+ rec.title +"</a></span></td>"+
                                "<td class='hide rec_id'>"+ rec.id +"</td>"+
                                "<td class='hide'>"+ rec.intro +"</td>"+
                                "<td><span>"+ rec.date +"</span></td>"+
                                "<td><button class='btn btn-mini btn-warning' onclick='modify_rec(this)'>修改</button></td>"+
                                "<td><button class='btn btn-mini btn-danger' onclick='deleteRec(this);'>删除</button></td>"+
                            "</tr>"
                            );
                    }
                    $("#rec_tbody").html(html);
                }
                else{
                    alert("没有更多");
                }
            }
            else
            {
                alert("请求失败！");
            }
        }
    );
}


function modify_link(obj)
{

    CURR_LINK_MOD_ID = $(obj).parent().prevAll().eq(1).text();
    initLinkModal(obj);
    $("#modify_link_modal").modal("show");
}

function initLinkModal(obj)
{
    name = $(obj).parent().siblings().find("a")[0].text;
    url = $(obj).parent().siblings().find("a")[0].href;
    level = $(obj).parent().prevAll().eq(0).find("span").text();
    $("#link_pop_name").val(name);
    $("#link_pop_link").val(url);
    $("#link_pop_level").val(level);
}

function setModLink()
{
    $("#pop_pub_link").click(function(){
        setCsrfHeader();
        $("#modify_link_modal").modal("hide");
        data = {
            "name":$("#link_pop_name").val(),
            "url":$("#link_pop_link").val(),
            "level":$("#link_pop_level").val(),
            "id":CURR_LINK_MOD_ID
        }
        $.post(
            "/index/admin/update_link/",
            data,
            function(data, status){
                if(data=="True" && status=="success")
                {
                    alert("modify link successfully");
                }
                else
                {
                    alert("failed to modify link");
                }
            }
        );
        return false;
    });
}


function delete_link(obj)
{
//    id = $(obj).parent().siblings().find("a")[0].text;
    setCsrfHeader();
    id = $(obj).parent().prevAll().eq(2).text();
    $.post(
        "/index/admin/delete_link/",
        {"id":id},
        function(data, status){
            if (status=="success" && data=="True")
            {
                alert("delete link successfullly");
            }
            else
            {
                alert("failed to delete link");
            }
        }
    );
    return false;

}




