class Chatbox{
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox_frame'),
            sendMessage: document.querySelector('.send_button')
        }

        this.messages = [];
    }

    display() {
        const {chatBox, sendMessage} = this.args;
        var console = window.console;

        sendMessage.addEventListener('click', () => this.onSendButton(chatBox)) // Checks if the send button is clicked

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter"){
                this.onSendButton(chatBox)
            }
        })

    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if(text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

        // Not giving a string?
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'            
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = {name: "Sibyl", message: r.answer};
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''
        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }

    updateChatText(chatbox){
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if(item.name === "Sibyl"){
                html += '<div class="message_item messages_item--visitor">' + item.message + '</div>'
            }
            else{
                html += '<div class="message_item messages_item--operator">' + item.message + '</div>'
            }
        });
        
        const chatmessage = chatbox.querySelector('.chatbox_messages');
        chatmessage.innerHTML = html;
    }

}

const chatbox = new Chatbox();
chatbox.display();