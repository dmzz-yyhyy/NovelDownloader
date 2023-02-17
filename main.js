window.addEventListener("load", function(){
    const button = document.getElementById("verifyButton");
    button.addEventListener("click", function (){
        const bookUrlInput = document.getElementById("bookUrlInput")
        let bookUrl = encodeURIComponent(bookUrlInput.value)
        let fileUrl = '/getBook?url=' + bookUrl + '&in_on_chapter_index=false'
        console.log(bookUrlInput.value)
        console.log(bookUrlInput.value.length)
        console.log(bookUrlInput.value.startsWith("https://www.52shuku.vip"))
        if (bookUrlInput.value.length > 0) {
            if (bookUrlInput.value.startsWith("https://www.52shuku.vip")) {
                document.getElementById("downloadUrl").href = fileUrl
                document.getElementById("downloadUrl").innerHTML = "点击下载"
                document.getElementById('error').innerHTML = ""
            }
            else {
                document.getElementById('error').innerHTML = "请输入网站www.52shuku.vip的小说链接"
                bookUrlInput.value = ''
            }
        }
        else {
            document.getElementById('error').innerHTML = "未输入小说链接"
            bookUrlInput.value = ''
        }

    })
    const input = document.getElementById("upLoadInput")
    input.addEventListener("click", function (){
        document.getElementById("isLoadFinish").innerHTML = "封面上传成功"
    })
})
function openHelp() {
    let helpDiv = document.getElementsByClassName("helpDiv")[0]
    helpDiv.style.display = 'flex'
    helpDiv.innerHTML = "<a id='closeHelp' onclick='closeHelp()'>关闭</a><h1>一.使用方法</h1><p>　　打开<a href='https://www.52shuku.vip/'>小说网站</a>然后再里面搜索一本需要打包的小说, 打开, 复制小说的介绍页的url, 如: https://www.52shuku.vip/yanqing/hpDs.html。再在本站输入。接着, 选择一个封面, 点击上传。最后按下确定即可完成打包。</p><h1>二.注意事项</h1><p>1.打包的个事为epub格式, 推荐使用NeatReader阅读器阅读。<br>2.必须上传封面，否则下载下来的电子书的封面可能会不对。<br>3.对本网站友好点，别弄崩了。。。</p>"
}
function closeHelp() {
    let helpDiv = document.getElementsByClassName("helpDiv")[0]
    helpDiv.style.display = 'none'
}