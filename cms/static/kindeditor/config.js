KindEditor.ready(function(K) {
    window.editor = K.create('#id_content',
        {
            'width':'800px',
            'height':'500px',
            'uploadJson': '/admin/upload/kindeditor',
        });
});

