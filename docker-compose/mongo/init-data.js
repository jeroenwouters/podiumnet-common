const conn = new Mongo();

const db = conn.getDB("podiumnet");

const dataToInsert = [
  {
    data: {},
    _id: "07a95db7-c909-4e37-9bba-219c99c721d9",
    identifiers: [
      "07a95db7-c909-4e37-9bba-219c99c721d9",
      "developers@inuits.eu",
    ],
    metadata: [
      { key: "idp_user_id", value: "developers@inuits.eu" },
      { key: "email", value: "developers@inuits.eu" },
    ],
    relations: [
      {
        key: "tenant:super",
        type: "hasTenant",
        roles: ["superAdmin"],
      },
    ],
    type: "user",
  },
  {
    data: {},
    _id: "tenant:super",
    identifiers: ["tenant:super"],
    metadata: [
      {
        key: "label",
        value: "SuperTenant",
      },
    ],
    relations: [
      {
        key: "developers@inuits.eu",
        type: "isTenantFor",
      },
    ],
    sort: {},
    type: "tenant",
  },
  {
    data: {},
    _id: "anonymous_user",
    identifiers: ["anonymous_user"],
    metadata: [],
    relations: [
      {
        key: "tenant:super",
        type: "hasTenant",
        roles: ["anonymous"],
      },
    ],
    type: "user",
  },
];

const collection = db.getCollection("entities");

const result = collection.insertMany(dataToInsert);

quit();
