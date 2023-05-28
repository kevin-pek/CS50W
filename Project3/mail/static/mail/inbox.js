window.onload = function() {
  const page = sessionStorage.getItem('page');

  if (page == 'inbox' || page == 'sent' ||page == 'archive') {
    load_mailbox(page)
  } else if (page == 'compose') {
    compose_email()
  } else {
    load_mailbox('inbox')
  }
}

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  sessionStorage.setItem('page', 'compose');

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function reply_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  console.log(this.dataset.id)
  fetch('/emails/'+this.dataset.id)
  .then(response => response.json())
  .then(email => {
    let recipient = email.sender;
    let subject = email.subject;
    if (!subject.startsWith("Re:")) {
      subject = "Re: "+subject;
    }
    let body = "On "+email.timestamp+" "+email.sender+" wrote: "+email.body;

    document.querySelector('#compose-recipients').value = recipient;
    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = body;
  })
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  sessionStorage.setItem('page', mailbox);

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //get emails
  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(item => {
      document.querySelector('#emails-view').innerHTML += `
                          <div id="email-container">
                          <button class="email-${item.read}" id=${item.id}>
                          <strong>${item.sender}</strong>
                          <b>${item.subject}</b>
                          <i>${item.timestamp}</i>
                          </button>
                          </div>`})

      //add event listeners to view email
      let buttons = document.querySelectorAll('#email-container > button')
      buttons.forEach(button => button.addEventListener('click', view_email))
  });
}

function view_email() {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  sessionStorage.setItem('page', 'inbox');

  //mark email as read
  fetch('/emails/'+this.id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch('/emails/'+this.id)
  .then(response => response.json())
  .then(email => {
    // Print email
    document.querySelector('#emails-view').innerHTML = `
        <h3>${email.subject}</h3>
        <strong>${email.sender}</strong><button data-id="${email.id}" class="btn btn-sm btn-outline-primary" id="archive">Add to Archive</button>
        <br />
        <i>sent at ${email.timestamp}</i>
        <br />
        to ${email.recipients}
        <hr />
        <p>${email.body}</p>
        <button data-id="${email.id}" class="btn btn-sm btn-outline-primary" id="reply">Reply</button>`;

    document.querySelector('#reply').addEventListener('click', reply_email);

    if (email.archived) {
      document.querySelector('#archive').innerHTML = "Remove from Archive";
    } else {
      document.querySelector('#archive').innerHTML = "Add to Archive";
    }

    if (email.sender == document.querySelector("#user_email").innerHTML) {
      document.querySelector('#archive').remove();
    } else {
      document.querySelector('#archive').addEventListener('click', archive_email);
    }
  });
}

function archive_email() {
  fetch('/emails/'+this.dataset.id)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    let isArchived = !email.archived;
    fetch('/emails/'+this.dataset.id, {
      method: 'PUT',
      body: JSON.stringify({
          archived: isArchived
      })
    })
    .then(location.reload())
  })

}

function send_email() {
  let email_recipients = document.querySelector('#compose-recipients').value;
  let email_subject = document.querySelector('#compose-subject').value;
  let email_body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: email_recipients,
         subject: email_subject,
        body: email_body
      })
    })
  .then(function() {
    sessionStorage.setItem('page', 'sent');
    load_mailbox('sent')
  })
}
