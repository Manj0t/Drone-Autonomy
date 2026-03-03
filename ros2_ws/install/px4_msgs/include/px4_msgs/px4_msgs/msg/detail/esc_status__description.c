// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from px4_msgs:msg/EscStatus.idl
// generated code does not contain a copyright notice

#include "px4_msgs/msg/detail/esc_status__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_px4_msgs
const rosidl_type_hash_t *
px4_msgs__msg__EscStatus__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x34, 0xa4, 0x7b, 0xca, 0x3d, 0x35, 0x84, 0x5d,
      0xa0, 0x1c, 0x50, 0xa8, 0xed, 0x5b, 0x87, 0x26,
      0xd3, 0x6a, 0x52, 0xed, 0xd7, 0x33, 0x6f, 0xe6,
      0x36, 0x35, 0x4a, 0xea, 0xf3, 0x44, 0xa6, 0xc9,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "px4_msgs/msg/detail/esc_report__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t px4_msgs__msg__EscReport__EXPECTED_HASH = {1, {
    0x16, 0x03, 0xec, 0x50, 0x5d, 0x34, 0x99, 0xde,
    0xbe, 0xcf, 0xea, 0xe5, 0xb0, 0xd1, 0x06, 0x39,
    0x4f, 0xa2, 0x2e, 0xec, 0xa3, 0x9f, 0x67, 0x8a,
    0x48, 0x48, 0x23, 0xe9, 0x3e, 0x5a, 0x98, 0x4a,
  }};
#endif

static char px4_msgs__msg__EscStatus__TYPE_NAME[] = "px4_msgs/msg/EscStatus";
static char px4_msgs__msg__EscReport__TYPE_NAME[] = "px4_msgs/msg/EscReport";

// Define type names, field names, and default values
static char px4_msgs__msg__EscStatus__FIELD_NAME__timestamp[] = "timestamp";
static char px4_msgs__msg__EscStatus__FIELD_NAME__counter[] = "counter";
static char px4_msgs__msg__EscStatus__FIELD_NAME__esc_count[] = "esc_count";
static char px4_msgs__msg__EscStatus__FIELD_NAME__esc_connectiontype[] = "esc_connectiontype";
static char px4_msgs__msg__EscStatus__FIELD_NAME__esc_online_flags[] = "esc_online_flags";
static char px4_msgs__msg__EscStatus__FIELD_NAME__esc_armed_flags[] = "esc_armed_flags";
static char px4_msgs__msg__EscStatus__FIELD_NAME__esc[] = "esc";

static rosidl_runtime_c__type_description__Field px4_msgs__msg__EscStatus__FIELDS[] = {
  {
    {px4_msgs__msg__EscStatus__FIELD_NAME__timestamp, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {px4_msgs__msg__EscStatus__FIELD_NAME__counter, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT16,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {px4_msgs__msg__EscStatus__FIELD_NAME__esc_count, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {px4_msgs__msg__EscStatus__FIELD_NAME__esc_connectiontype, 18, 18},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {px4_msgs__msg__EscStatus__FIELD_NAME__esc_online_flags, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {px4_msgs__msg__EscStatus__FIELD_NAME__esc_armed_flags, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {px4_msgs__msg__EscStatus__FIELD_NAME__esc, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_ARRAY,
      8,
      0,
      {px4_msgs__msg__EscReport__TYPE_NAME, 22, 22},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription px4_msgs__msg__EscStatus__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {px4_msgs__msg__EscReport__TYPE_NAME, 22, 22},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
px4_msgs__msg__EscStatus__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {px4_msgs__msg__EscStatus__TYPE_NAME, 22, 22},
      {px4_msgs__msg__EscStatus__FIELDS, 7, 7},
    },
    {px4_msgs__msg__EscStatus__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&px4_msgs__msg__EscReport__EXPECTED_HASH, px4_msgs__msg__EscReport__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = px4_msgs__msg__EscReport__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint64 timestamp\\t\\t\\t\\t\\t# time since system start (microseconds)\n"
  "uint8 CONNECTED_ESC_MAX = 8\\t\\t\\t\\t# The number of ESCs supported. Current (Q2/2013) we support 8 ESCs\n"
  "\n"
  "uint8 ESC_CONNECTION_TYPE_PPM = 0\\t\\t\\t# Traditional PPM ESC\n"
  "uint8 ESC_CONNECTION_TYPE_SERIAL = 1\\t\\t\\t# Serial Bus connected ESC\n"
  "uint8 ESC_CONNECTION_TYPE_ONESHOT = 2\\t\\t\\t# One Shot PPM\n"
  "uint8 ESC_CONNECTION_TYPE_I2C = 3\\t\\t\\t# I2C\n"
  "uint8 ESC_CONNECTION_TYPE_CAN = 4\\t\\t\\t# CAN-Bus\n"
  "uint8 ESC_CONNECTION_TYPE_DSHOT = 5\\t\\t\\t# DShot\n"
  "\n"
  "uint16 counter  \\t\\t\\t\\t\\t# incremented by the writing thread everytime new data is stored\n"
  "\n"
  "uint8 esc_count\\t\\t\\t\\t\\t\\t# number of connected ESCs\n"
  "uint8 esc_connectiontype\\t\\t\\t\\t# how ESCs connected to the system\n"
  "\n"
  "uint8 esc_online_flags\\t\\t\\t\\t\\t# Bitmask indicating which ESC is online/offline\n"
  "# esc_online_flags bit 0 : Set to 1 if ESC0 is online\n"
  "# esc_online_flags bit 1 : Set to 1 if ESC1 is online\n"
  "# esc_online_flags bit 2 : Set to 1 if ESC2 is online\n"
  "# esc_online_flags bit 3 : Set to 1 if ESC3 is online\n"
  "# esc_online_flags bit 4 : Set to 1 if ESC4 is online\n"
  "# esc_online_flags bit 5 : Set to 1 if ESC5 is online\n"
  "# esc_online_flags bit 6 : Set to 1 if ESC6 is online\n"
  "# esc_online_flags bit 7 : Set to 1 if ESC7 is online\n"
  "\n"
  "uint8 esc_armed_flags\\t\\t\\t\\t\\t# Bitmask indicating which ESC is armed. For ESC's where the arming state is not known (returned by the ESC), the arming bits should always be set.\n"
  "\n"
  "EscReport[8] esc";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
px4_msgs__msg__EscStatus__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {px4_msgs__msg__EscStatus__TYPE_NAME, 22, 22},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 1376, 1376},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
px4_msgs__msg__EscStatus__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *px4_msgs__msg__EscStatus__get_individual_type_description_source(NULL),
    sources[1] = *px4_msgs__msg__EscReport__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
