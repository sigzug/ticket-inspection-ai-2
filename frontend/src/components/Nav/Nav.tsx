import {Box, Flex, HStack, Link, Spacer, Text} from "@chakra-ui/react";
import {BACKEND} from "../../globals.ts";

export const Nav = () => {
    return (
        <Box as="nav" bg="#00685e" px="6" py="3" shadow="sm" borderRadius="md" m={2}>
            <Flex align="center">
                <Text fontWeight="bold" fontSize="xl" color={"white"}>FY</Text>

                <HStack ml="10" display={{base: "none", md: "flex"}}>
                    <Link href="/">Use Model</Link>
                </HStack>

                <Spacer/>

                <HStack>
                    <Link href={`${BACKEND}/admin/`} rel="noopener">Admin</Link>
                </HStack>
            </Flex>
        </Box>
    );
}
