$(function() {

    // 获取个人信息
    var avatar = $('.avatar');
    var nickname = $('.nickname');
    var sign = $('.sign');


    var getUrlParams = function(url) {
        var queryString = url.split('?')[1];
        var queryParams = {};
        if(queryString) {
            var pairs = queryString.split('&');
            for(var i = 0; i < pairs.length; i++) {
                var tmp = pairs[i].split('=');
                queryParams[tmp[0]] = tmp[1];
            }
        }
        return queryParams;
    }


    $.ajax({
        url: 'http://nbstorage.sparta.html5.qq.com/user/profile/info', 
        type: 'POST',
        contentType: 'application/json',
        data: getUrlParams(window.location.href),
        success: function(res){
            if(res && res.msg === '成功') {
                var data = res.data;
                avatar.attr('src', data.profile.icon)
                nickname.val(data.profile.nickname)
                sign.val(data.profile.signature)
            } else {
                console.log('获取个人信息错误！')
            }
        }
    })

    // 编辑
    var fileBtn = $('.file-btn');
    var inputfile = $('.file-input');

    // 选择文件
    // fileBtn.on('click', function(){
    //     inputfile.click()
    // })

    // inputfile.on('change', function(val){
    //     console.log(val)

    // })

    // 提交
    var saveBtn = $('#save')
    saveBtn.on('click', function() {
        var nicknameVal = nickname.val();
        if(nicknameVal.length <= 0 || nicknameVal.length > 12) {
            return console.log('nickname 长度不符合要求')
        }

        var signVal = sign.val();
        var params = {
            nickname: nicknameVal,
            sign: signVal
        }
        // 保存接口
        // $.ajax({
        //     url: '',
        //     data: params,
        //     success: function(res) {
        //         if(res && res.sucess) {

        //         } else {

        //         }
        //     }
        // })        

    })

})