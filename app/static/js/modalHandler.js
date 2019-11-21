/**
* @file modalHandler.js : handles the creation of modals from a list of posts within a gallery
* @version 1
* @author David Knox 
*/

/**
* post HTMLElement format: {
*   <article class="post">
*        <figure>
*           <img src="link.img" alt="title">
*           <figcaption> Title </figcaption>
*        </figure>
*        <h3 class="author"> Author Name </h3>
*        <p> Description blah blah blah </p>
*   </article>
* }
 */

// Main Code Block which is run upon loading of the script
{
    "use strict";

    // Importing posts and sending them to exPosts
    const posts = [...document.getElementsByClassName('post')];
    const images = exPosts(posts);

    // Adding event listener to append modal to 
    images.forEach(image => {
        image.postImg.addEventListener('click', () => document.body.appendChild(makeModal(image)));
    });
}
/**
 * exPosts() function which takes an array of post elements and returns an array of image objects
 * @param {array} posts - an array of posts which follow the format defined at the top of this document
 * @returns {array} images - an array of image objects
 */
function exPosts(posts) {

    // Mapping the posts into postObjer() function
    const images = posts.map(post => {
        const image = post.getElementsByTagName('img')[0];
        // Creating the image object
        imgObj = {

            // Importing values from the post element
            'postImg': image,
            'link': image.src
        }
        return imgObj
    }
    );
    return images
}

/**
 * makeModal() function which takes an image object and returns a modal element.
 * @param {object} image - image object with postImg and link attributes.
 * @returns {HTMLElement} modal - modal element with an X button and the image provided.
 */
function makeModal(image) {

    // Create elements
    const modal = document.createElement('section');
    const imgEl = document.createElement('img');
    const exBut = document.createElement('button');

    // Add X button which destroys the modal element
    exBut.innerText = 'X';
    exBut.addEventListener('click', e => e.target.parentNode.remove());

    // Add modal class to main modal element
    modal.classList.add('modal');

    // Set image source to image object property
    imgEl.src = image.link;

    // Add elements to main modal element
    modal.appendChild(imgEl);
    modal.appendChild(exBut);
    
    // FINALLY return the modal element
    return modal
}