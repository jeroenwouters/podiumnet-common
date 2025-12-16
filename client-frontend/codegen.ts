import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  overwrite: true,
  schema: [
    "./inuits-dams-graphql-service/modules/*/*.schema.ts",
    "./inuits-dams-graphql-service/modules/*/baseModule/*.schema.ts",
    "./inuits-dams-graphql-service/src/*.schema.ts",
    "./modules/*/*.schema.ts",
    "./modules/*/baseModule/*.schema.ts",
  ],
  documents: [
    "./inuits-dams-graphql-service/src/queries/*.queries.ts",
    "./inuits-dams-graphql-service/src/queries/*/*.queries.ts",
    "./inuits-dams-graphql-service/src/queries/*/*/*.queries.ts",
    "./inuits-dams-graphql-service/modules/*/queries/*.queries.ts",
    "./inuits-dams-graphql-service/modules/*/baseModule/queries/*.queries.ts",
    "./modules/*/queries/*.queries.ts",
    "./modules/*/baseModule/queries/*.queries.ts",
  ],
  generates: {
    "inuits-dams-pwa/src/generated-types/queries.ts": {
      plugins: [
        {
          add: {
            content:
              "/* eslint-disable */\n// THIS FILE IS GENERATED, DO NOT EDIT!",
          },
        },
        { typescript: {} },
        { "typescript-operations": {} },
        { "typed-document-node": {} },
      ],
    },
    "inuits-dams-graphql-service/generated-types/type-defs.ts": {
      plugins: [
        {
          add: {
            content: "// THIS FILE IS GENERATED, DO NOT EDIT!",
          },
        },
        { typescript: {} },
        { "typescript-resolvers": {} },
      ],
    },
  },
  config: {
    preResolveTypes: true,
    scalars: { Void: "void" },
    useTypeImports: true,
    dedupeFragments: true,
  },
};

export default config;
