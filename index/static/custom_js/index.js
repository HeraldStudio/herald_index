/**
 * Created with PyCharm.
 * User: wolf
 * Date: 13-10-22
 * Time: 下午1:22
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function(){
    developingWarning();
});




function developingWarning()
{
    $(".developing").click(function(){
        alert("开发中...");
        return false;
    });

}





