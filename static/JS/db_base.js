/**
 * Created by luojie on 2017/4/9.
 */

//复选框事件
//全选、取消全选的事件
function selectAll(){
    if ($("#SelectAll").prop("checked")) {
        $(".subcheck").prop("checked", true);
    } else {
        $(".subcheck").prop("checked", false);
    }
}
//子复选框的事件
function setSelectAll(){
    //当没有选中某个子复选框时，SelectAll取消选中
    if (!$(".subcheck").checked) {
        $("#SelectAll").prop("checked", false);
    }
    var chsub = $(".subcheck").length; //获取subcheck的个数
    var checkedsub = $(".subcheck:checked").length; //获取选中的subcheck的个数
    if (checkedsub == chsub) {
        $("#SelectAll").prop("checked", true);
    }
}
