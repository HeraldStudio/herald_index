/**
 * Created with PyCharm.
 * User: wolf
 * Date: 13-10-22
 * Time: 下午1:22
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function(){
    developingWarning();
    setAppClick();
});




function developingWarning()
{
    $(".developing").click(function(){
        alert("开发中...");
        return false;
    });

}


function setAppClick()
{
    $(".app_module").click(function(){
        appname = $(this).attr("app_name");
        alert(appname);
        if(appname=="先声")
        {
            showAndroidModal();
        }
        if(appname=="小猴偷米")
        {
            showChatsModal();
        }
        return false;
    });
}

function showChatsModal()
{
        $('#chatsmodal').modal('show');
}

function showAndroidModal()
{
    $("#androidmodal").modal("show");
}





