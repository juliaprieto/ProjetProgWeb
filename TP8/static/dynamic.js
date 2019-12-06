function main(){


  function filter_domains(input_element) {

      let all_tr = document.querySelector("tbody").children;
      for (let line of all_tr) {

        content = line.children[1].textContent
        if ( ! content.includes(balise_input.value)) {
          line.style["display"]="None"
        }
        else {
          line.style["display"]=null
        }

      }
    // console.log(line.children[1].textContent)
  }

  balise_input = document.getElementById("domain_filter")
  balise_input.addEventListener("input",function(){filter_domains(balise_input)})
  console.log("Coucou")
}

main();
