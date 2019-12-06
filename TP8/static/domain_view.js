function main(){


  // function class_from_table(){
  //   table2.children[0].classList
  // }



    // let table1 = document.querySelectorAll("tbody")[1]
    //
    // for (let line of table1.children){
    //   line.addEventListener("mouseenter", mouseenter_Table1)
    // }
    //   function mouseenter_Table1(evt){
    //     let table2 = document.querySelectorAll("tbody")[2]
    //     evt.target.classList.add("highlight");
    //     for (let line2 of table2.children){
    //       if (line2.classList.contains(evt.target.id)){
    //         line2.classList.add("highlight")
    //       }
    //     }
    //     }


  function mouseenter_Table1(){
    let table1 = document.querySelectorAll("tbody")[1]
    let table2 = document.querySelectorAll("tbody")[2]
    for (let line of table1.children){
      line.addEventListener("mouseenter", (evt) => {
        line.classList.add("highlight");
        for (let line2 of table2.children){
          if (line2.classList.contains(evt.target.id)){
            line2.classList.add("highlight")
          }
        }
      })
    }
  }

  function mouseenter_Table2(){
    let table1 = document.querySelectorAll("tbody")[1]
    let table2 = document.querySelectorAll("tbody")[2]

    for (let line of table2.children){
      line.addEventListener("mouseenter", (evt) => {
      line.classList.add("highlight");
        for (let line2 of table1.children){
          if (evt.target.classList.contains(line2.id)){
            line2.classList.add("highlight")
          }
        }
      })
    }
  }

  function mouseleave_Table1(){
    let table1 = document.querySelectorAll("tbody")[1]
    let table2 = document.querySelectorAll("tbody")[2]

    for (let line of table1.children){
      line.addEventListener("mouseleave", (evt) => {
        for (let line2 of table2.children){
          line.classList.remove("highlight");
          if (line2.classList.contains(evt.target.id)){
            line2.classList.remove("highlight");
          }
        }
      })
    }
  }


  function mouseleave_Table2(){
    let table1 = document.querySelectorAll("tbody")[1]
    let table2 = document.querySelectorAll("tbody")[2]

    for (let line of table2.children){
      line.addEventListener("mouseleave", (evt) => {
      line.classList.remove("highlight");
        for (let line2 of table1.children){
          if (evt.target.classList.contains(line2.id)){
            line2.classList.remove("highlight")
          }
        }
      })
    }
  }
// mouseenter_Table1()
mouseenter_Table1()
mouseenter_Table2()
mouseleave_Table1()
mouseleave_Table2()



  function display_description(){
    let table1 = document.querySelectorAll("tbody")[1]
    for (let line of table1.children){
      cell=line.children[1];
      cell.addEventListener("click", (evt)=>{
        let ID_domain = evt.target.parentNode.id;
        fetch(ID_domain + ".json")
        .then((resp) => {
          if (!resp.ok) { throw("Error " + resp.status); }
          return resp.json();
        }).then((data) => {

          text_box=document.querySelector(".dialog");
          text_box.innerHTML=`<h2> Description of domain <em>${data.description}</em> </h2>`
          // text_box.innerHTML(<ul><li></li>)
          function InnerHTML(box, data){
            let ul_element=document.createElement("ul")

            for (const property in data) {
              if (property !== "description"){
              const maj_property = property.charAt(0).toUpperCase() + property.slice(1)
              let li_element=document.createElement("li");
              if (property !== "proteins"){
                li_element.textContent= `${maj_property}: ${data[property]}`
              }
              else {
                li_element.textContent= `${maj_property}: ${data[property].join(", ")}`
              }
              ul_element.appendChild(li_element)

            }
          }
            text_box.appendChild(ul_element)

          }
          InnerHTML(text_box, data)
          text_box.style.maxHeight="8em";
          text_box.style.backgroundColor="white"
          text_box.style.borderColor = "lightBlue"
          text_box.style.width="30em";
          text_box.style.padding="2em";
          text_box.style.overflowY="scroll";
          text_box.style.display="inline-block";

          // data contient les données JSON (sous forme d'un objet)
          // AJOUTEZ ICI le code Javascript qui traite ces données
        }).catch((err) => {
          console.error(err);
        });

      })
    }

  }

  display_description()
  console.log("Coucou")
}

main();
