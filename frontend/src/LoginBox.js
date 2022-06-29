import React, {useEffect, useState} from 'react';
import {Box, Button, Center, FormControl, Input, Text, VStack} from '@chakra-ui/react';
import {Form, Formik} from "formik";
import Config from './Config';

const tokenApi = Config.api+'users/token/';

const getToken = async (username, password)=>{

    const response = await fetch(tokenApi, {
        body: `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`,
        headers: {
            Accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method: "POST"
        });
    const data = await response.json();
    alert("Your token is: "+data.access_token+"\n\nIt will expire in 900 seconds");
    localStorage.setItem('accessToken', data.access_token);
    return data.access_token;
}

const LoginBox = props => (
    document.title='Login',
    <Center>
    <Box p='4' maxW='lg' textAlign="left">
        <Text fontSize="2xl" mb="5">Login in for more functionality</Text>
        <Formik
            initialValues={{ username: '', password: '' }}
            validate={values => {
                const errors = {};
                if (!values.username) {
                    errors.username = 'Required';
                } else if (values.username.length < 3) {
                    errors.email = 'Username too short';
                }
                return errors;
            }}
            onSubmit={(values, { setSubmitting }) => {
                const accessToken = getToken(values.username, values.password);
                setTimeout(() => {
                    console.log(JSON.stringify(values, null, 2));
                    setSubmitting(false);
                    }, 400);
            }}
        >
        {({
            values,
            errors,
            touched,
            handleChange,
            handleBlur,
            handleSubmit,
            isSubmitting,
            /* and other goodies */
        }) => (
            <Form onSubmit={handleSubmit}>
            <VStack>
            <Input
                width = '80%'
                type="text"
                name="username"
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.username}
                placeholder='username/用戶名'
            />
            {errors.email && touched.email && errors.email}

            <Input
                width = '80%'
                type="password"
                name="password"
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.password}
                placeholder='password/密碼'
            />
            {errors.password && touched.password && errors.password}

            <Button type="submit" disabled={isSubmitting} mt="5">
                Submit
            </Button>
            </VStack>
            </Form>
        )}
        </Formik>
      </Box>	
      </Center>
);	

export default LoginBox;
