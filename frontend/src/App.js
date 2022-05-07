import React, {useEffect, useState} from 'react';
import {useFormik,Formik,Field,Form} from 'formik';
import DataTable from './table';
import {
  ChakraProvider,
  Button,
  Box,
  Text,
  Link,
  VStack,
  Input,
  Grid,
  theme,
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import { Logo } from './Logo';


function App() {
	
   const [isLoading,setLoading] = useState(true);
   const [data, setData] = useState([]);
   const [target, setTarget] = useState([]);
   const makeData = (words,probs)=>{
	   let results = [];
	   for(let i=0;i<words.length;i++){
	   	results.push({word:words[i],prob:probs[i]});
	   }
	   return results
   }  

   const getList = async (target)=>{
	   try{
		var url = 'http://127.0.0.1:8000/related/'+target;
		const response = await fetch(url,{method:'POST'})
		const json = await response.json();
		console.log(json);
		var results = makeData(json.words,json.probs);
		console.log(results);
	        setData(results);
	   }catch(error){console.error(error);
	   }finally{
		setLoading(false);
	   }
	}

    useEffect(() => {
	    getList(target);
 	 }, []);
  
   const SearchForm=()=>{
        const formik = useFormik({
         initialValues:{
                word: 'whatever',
          },
		onSubmit:(values,actions)=>{
			actions.setSubmitting(false);
			getList(target);
			setTarget(values.word);
			console.log(values.word);
	  },
		onChange: (values,actions)=>{
                        setTarget(values.word);
                        console.log(values.word);
                        getList(target);
			actions.setSubmitting(false);
	  
	  },
        });
        return(
        <form onSubmit = {formik.handleSubmit}>
         <label htmlFor='word'>Word Searched For</label>
         <Input
            id ='word'
            name = 'word'
            type = 'word'
            onChange = {formik.handleChange}
            value = {formik.values.word}
        />
        <Button type="submit">Submit</Button>
        </form>
        );
    };

  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <VStack spacing={8}>
            <Logo h="15vmin" pointerEvents="none" /> 
          <SearchForm/>
	  <DataTable data={data}/>
	  </VStack>
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;
