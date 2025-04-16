from app.services.llm_service import ai_engine

all_file = """
{
  "birth_certificate": {                       // 加拿大出生证明信息
    "certificate_number": "123456789",          // 证书编号
    "issued_by": "Ontario Ministry of Health",  // 签发机构：安大略省卫生部
    "issue_date": "15 FEB 2015",                // 签发日期
    "certificate_type": "Certified",            // 证书类型：认证出生证明
    "holder_information": {                     // 持卡人信息
      "first_name": "Emily",                    // 名字
      "last_name": "Smith",                     // 姓氏
      "middle_name": "Rose",                    // 中间名
      "date_of_birth": "12 JAN 1990",           // 出生日期
      "place_of_birth": "Toronto, Ontario",     // 出生地点
      "sex": "Female",                          // 性别
      "nationality": "Canada",                  // 国籍
      "citizenship_status": "Canadian Citizen", // 公民身份：加拿大公民
      "address": {                              // 持卡人地址
        "street": "123 Maple Rd",               // 街道地址
        "city": "Toronto",                      // 城市
        "province": "Ontario",                  // 省份
        "postal_code": "M5A 1B2"                // 邮政编码
      }
    },
    "parent_information": {                     // 父母信息
      "father": {
        "first_name": "John",                   // 父亲名字
        "last_name": "Smith",                   // 父亲姓氏
        "birth_date": "05 DEC 1965",            // 父亲出生日期
        "place_of_birth": "Ottawa, Ontario"     // 父亲出生地点
      },
      "mother": {
        "first_name": "Sarah",                  // 母亲名字
        "last_name": "Smith",                   // 母亲姓氏
        "birth_date": "10 MAR 1968",            // 母亲出生日期
        "place_of_birth": "Montreal, Quebec"    // 母亲出生地点
      }
    },
    "document_category": "Birth Certificate"   // 文件类别：出生证明
  }
}
{
  "work_permit": {                           // 加拿大工作许可证信息
    "permit_number": "123456789",             // 工作许可证编号
    "issued_by": "Immigration, Refugees and Citizenship Canada", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "10 MAR 2021",              // 签发日期
    "expiry_date": "10 MAR 2023",             // 到期日期
    "permit_type": "Open Work Permit",        // 许可证类型：开放工作许可证
    "status": "Active",                       // 状态：有效
    "holder_information": {                   // 持卡人信息
      "first_name": "James",                  // 名字
      "last_name": "Brown",                   // 姓氏
      "middle_name": "T",                     // 中间名（可选）
      "date_of_birth": "22 JUN 1985",         // 出生日期
      "place_of_birth": "Vancouver, BC",      // 出生地点
      "sex": "Male",                          // 性别
      "nationality": "USA",                   // 国籍
      "passport_number": "X12345678",         // 护照号码
      "passport_issued_by": "U.S. Department of State", // 护照签发机构
      "address": {                             // 持卡人地址
        "street": "456 Oak Ave",              // 街道地址
        "city": "Toronto",                    // 城市
        "province": "ON",                     // 省份
        "postal_code": "M5A 1B2"              // 邮政编码
      }
    },
    "employer_information": {                 // 雇主信息
      "employer_name": "Tech Innovations Ltd.",// 雇主公司名称
      "company_address": {                     // 雇主地址
        "street": "789 Tech Park Dr",         // 公司街道地址
        "city": "Ottawa",                     // 公司城市
        "province": "ON",                     // 公司省份
        "postal_code": "K1A 0B1"              // 公司邮政编码
      },
      "job_title": "Software Developer",      // 工作职位
      "job_description": "Developing software applications.", // 工作描述
      "work_location": "Toronto, ON"          // 工作地点
    },
    "security_features": [                    // 安全特征
      "Barcode",                              // 条形码
      "Hologram",                              // 全息图
      "Magnetic Stripe"                        // 磁条
    ],
    "document_category": "Work Permit"       // 文件类别：工作许可证
  }
}
{
  "citizenship_proof": {                           // 加拿大公民身份证明
    "document_type": "Canadian Citizenship Card",   // 文件类型：加拿大公民卡
    "card_number": "1234-5678-90",                  // 公民卡号
    "issued_by": "Immigration, Refugees and Citizenship Canada", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "15 JUL 2010",                    // 签发日期
    "expiry_date": "15 JUL 2020",                   // 到期日期
    "status": "Expired",                            // 状态：已过期
    "holder_information": {                         // 持卡人信息
      "first_name": "David",                        // 名字
      "last_name": "Williams",                      // 姓氏
      "middle_name": "Joseph",                      // 中间名
      "date_of_birth": "10 DEC 1985",               // 出生日期
      "place_of_birth": "Vancouver, BC",            // 出生地点
      "sex": "Male",                                // 性别
      "nationality": "Canada",                      // 国籍：加拿大
      "citizenship_status": "Canadian Citizen",     // 公民身份：加拿大公民
      "address": {                                  // 持卡人地址
        "street": "101 Maple Ave",                  // 街道地址
        "city": "Vancouver",                        // 城市
        "province": "BC",                           // 省份
        "postal_code": "V5K 0A1"                    // 邮政编码
      }
    },
    "security_features": [                          // 安全特征
      "Hologram",                                   // 全息图
      "Barcode",                                    // 条形码
      "Magnetic Stripe"                             // 磁条
    ],
    "document_category": "Canadian Citizenship Proof" // 文件类别：加拿大公民身份证明
  }
}
{
  "citizenship_certificate": {                  // 加拿大国籍证书
    "certificate_number": "CIT123456789",        // 证书编号
    "issued_by": "Immigration, Refugees and Citizenship Canada", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "12 JUN 2018",                 // 签发日期
    "holder_information": {                      // 持卡人信息
      "first_name": "Ava",                       // 名字
      "last_name": "Johnson",                    // 姓氏
      "middle_name": "Marie",                    // 中间名（可选）
      "date_of_birth": "15 SEP 1990",            // 出生日期
      "place_of_birth": "Montreal, Quebec",      // 出生地点
      "sex": "Female",                           // 性别
      "nationality": "Canada",                   // 国籍：加拿大
      "citizenship_status": "Canadian Citizen",  // 公民身份：加拿大公民
      "address": {                               // 持卡人地址
        "street": "987 Birch St",                // 街道地址
        "city": "Vancouver",                     // 城市
        "province": "BC",                        // 省份
        "postal_code": "V6B 1A4"                 // 邮政编码
      }
    },
    "security_features": [                       // 安全特征
      "Hologram",                                // 全息图
      "Barcode",                                 // 条形码
      "Magnetic Stripe"                          // 磁条
    ],
    "document_category": "Canadian Citizenship Certificate" // 文件类别：加拿大国籍证书
  }
}
{
  "international_driving_permit": {              // 加拿大国际驾驶许可证
    "permit_number": "IDP123456789",              // 许可证编号
    "issued_by": "Canadian Automobile Association (CAA)", // 签发机构：加拿大汽车协会（CAA）
    "issue_date": "15 MAY 2021",                  // 签发日期
    "expiry_date": "15 MAY 2023",                 // 到期日期
    "permit_type": "International Driving Permit", // 许可证类型：国际驾驶许可证
    "holder_information": {                       // 持卡人信息
      "first_name": "Olivia",                     // 名字
      "last_name": "Taylor",                      // 姓氏
      "middle_name": "Marie",                     // 中间名（可选）
      "date_of_birth": "22 AUG 1985",             // 出生日期
      "place_of_birth": "Toronto, Ontario",       // 出生地点
      "sex": "Female",                            // 性别
      "nationality": "Canada",                    // 国籍：加拿大
      "driver_license_number": "ON1234567",       // 驾驶执照号码（本地）
      "license_issued_by": "Ontario Ministry of Transportation", // 本地执照签发机构
      "address": {                                // 持卡人地址
        "street": "789 Elm St",                   // 街道地址
        "city": "Ottawa",                         // 城市
        "province": "ON",                         // 省份
        "postal_code": "K1A 0B2"                  // 邮政编码
      }
    },
    "document_category": "International Driving Permit", // 文件类别：国际驾驶许可证
    "security_features": [                        // 安全特征
      "Barcode",                                  // 条形码
      "Hologram",                                  // 全息图
      "Watermark"                                  // 水印
    ]
  }
}
{
  "canadian_passport": {                        // 加拿大护照信息
    "passport_number": "AB1234567",              // 护照号码
    "issued_by": "Immigration, Refugees and Citizenship Canada", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "1 JAN 2020",                  // 签发日期
    "expiry_date": "1 JAN 2030",                 // 到期日期
    "passport_type": "Regular",                  // 护照类型：常规护照
    "holder_information": {                       // 持卡人信息
      "first_name": "John",                      // 名字
      "last_name": "Doe",                        // 姓氏
      "middle_name": "William",                  // 中间名（可选）
      "date_of_birth": "15 MAR 1985",            // 出生日期
      "place_of_birth": "Toronto, Ontario",      // 出生地点
      "sex": "Male",                             // 性别
      "nationality": "Canada",                   // 国籍：加拿大
      "citizenship_status": "Canadian Citizen",  // 公民身份：加拿大公民
      "address": {                                // 持卡人地址
        "street": "123 Maple St",                 // 街道地址
        "city": "Ottawa",                         // 城市
        "province": "ON",                         // 省份
        "postal_code": "K1A 0B1"                  // 邮政编码
      }
    },
    "security_features": [                       // 安全特征
      "Hologram",                                // 全息图
      "Barcode",                                 // 条形码
      "Magnetic Stripe"                          // 磁条
    ],
    "document_category": "Passport"              // 文件类别：护照
  }
}
{
  "canadian_driver_license": {                  // 加拿大驾驶执照信息
    "license_number": "A1234567",                // 驾驶执照号码
    "issued_by": "Ontario Ministry of Transportation", // 签发机构：安大略省交通部
    "issue_date": "10 FEB 2019",                 // 签发日期
    "expiry_date": "10 FEB 2024",                // 到期日期
    "license_type": "Class G",                   // 驾驶执照类型：G类（通常是普通驾驶执照）
    "holder_information": {                      // 持卡人信息
      "first_name": "Emma",                      // 名字
      "last_name": "Johnson",                    // 姓氏
      "middle_name": "Grace",                    // 中间名（可选）
      "date_of_birth": "5 NOV 1990",             // 出生日期
      "place_of_birth": "Toronto, Ontario",      // 出生地点
      "sex": "Female",                           // 性别
      "nationality": "Canada",                   // 国籍：加拿大
      "address": {                               // 持卡人地址
        "street": "456 Oak St",                  // 街道地址
        "city": "Ottawa",                        // 城市
        "province": "ON",                        // 省份
        "postal_code": "K2P 2C3"                 // 邮政编码
      }
    },
    "vehicle_categories": [                      // 可驾驶的车辆类别
      "Passenger Vehicles",                      // 乘用车
      "Motorcycles"                              // 摩托车
    ],
    "security_features": [                       // 安全特征
      "Barcode",                                 // 条形码
      "Hologram",                                // 全息图
      "Magnetic Stripe"                          // 磁条
    ],
    "document_category": "Driver's License"      // 文件类别：驾驶执照
  }
}
{
  "canadian_health_card": {                    // 加拿大健康卡信息
    "health_card_number": "1234 5678 9101",     // 健康卡号码
    "issued_by": "Ontario Health Insurance Plan (OHIP)", // 签发机构：安大略省健康保险计划（OHIP）
    "issue_date": "15 MAR 2021",                // 签发日期
    "expiry_date": "15 MAR 2026",               // 到期日期
    "holder_information": {                     // 持卡人信息
      "first_name": "Sophia",                   // 名字
      "last_name": "Brown",                     // 姓氏
      "middle_name": "Grace",                   // 中间名（可选）
      "date_of_birth": "12 AUG 1987",           // 出生日期
      "place_of_birth": "Vancouver, BC",        // 出生地点
      "sex": "Female",                          // 性别
      "nationality": "Canada",                  // 国籍：加拿大
      "address": {                              // 持卡人地址
        "street": "789 Pine St",                // 街道地址
        "city": "Toronto",                      // 城市
        "province": "ON",                       // 省份
        "postal_code": "M5G 2C5"                // 邮政编码
      }
    },
    "health_plan": "OHIP",                      // 医疗保险计划名称（如OHIP）
    "document_category": "Health Card",         // 文件类别：健康卡
    "security_features": [                      // 安全特征
      "Barcode",                                // 条形码
      "Hologram",                               // 全息图
      "Magnetic Stripe"                         // 磁条
    ]
  }
}
{
  "canadian_temporary_work_permit": {            // 加拿大临时工作证信息
    "permit_number": "TW123456789",               // 工作许可证编号
    "issued_by": "Immigration, Refugees and Citizenship Canada (IRCC)", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "20 FEB 2022",                  // 签发日期
    "expiry_date": "20 FEB 2024",                 // 到期日期
    "permit_type": "Temporary Work Permit",       // 许可证类型：临时工作证
    "holder_information": {                       // 持证人信息
      "first_name": "Maria",                      // 名字
      "last_name": "Smith",                       // 姓氏
      "middle_name": "Elena",                     // 中间名（可选）
      "date_of_birth": "10 JUL 1990",             // 出生日期
      "place_of_birth": "Mexico City, Mexico",    // 出生地点
      "sex": "Female",                            // 性别
      "nationality": "Mexico",                    // 国籍：墨西哥
      "address": {                                // 持证人地址
        "street": "1234 Maple Ave",               // 街道地址
        "city": "Vancouver",                      // 城市
        "province": "BC",                         // 省份
        "postal_code": "V5K 1A1"                  // 邮政编码
      }
    },
    "employment_details": {                       // 雇佣详情
      "employer_name": "ABC Company",             // 雇主名称
      "job_title": "Software Developer",          // 职位名称
      "job_location": "Vancouver, BC",            // 工作地点
      "start_date": "1 MAR 2022",                 // 工作开始日期
      "end_date": "1 MAR 2024"                    // 工作结束日期
    },
    "security_features": [                        // 安全特征
      "Barcode",                                  // 条形码
      "Hologram",                                 // 全息图
      "Magnetic Stripe"                           // 磁条
    ],
    "document_category": "Temporary Work Permit"  // 文件类别：临时工作证
  }
}
{
  "canadian_temporary_resident_visa": {         // 加拿大临时居民签证信息
    "visa_number": "TRV123456789",               // 签证号码
    "issued_by": "Immigration, Refugees and Citizenship Canada (IRCC)", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "1 JAN 2023",                  // 签发日期
    "expiry_date": "1 JAN 2024",                 // 到期日期
    "visa_type": "Temporary Resident Visa",      // 签证类型：临时居民签证
    "holder_information": {                      // 持证人信息
      "first_name": "Oliver",                    // 名字
      "last_name": "Taylor",                     // 姓氏
      "middle_name": "James",                    // 中间名（可选）
      "date_of_birth": "20 JUN 1985",            // 出生日期
      "place_of_birth": "London, UK",            // 出生地点
      "sex": "Male",                             // 性别
      "nationality": "United Kingdom",           // 国籍：英国
      "address": {                               // 持证人地址
        "street": "123 Park Lane",               // 街道地址
        "city": "Vancouver",                     // 城市
        "province": "BC",                        // 省份
        "postal_code": "V6B 1A1"                 // 邮政编码
      }
    },
    "visa_conditions": {                         // 签证条件
      "purpose_of_visit": "Tourism",             // 访问目的：旅游
      "validity_period": "6 months",             // 有效期：6个月
      "entry_multiple": true                     // 是否为多次入境：是
    },
    "security_features": [                       // 安全特征
      "Barcode",                                 // 条形码
      "Hologram",                                // 全息图
      "Magnetic Stripe"                          // 磁条
    ],
    "document_category": "Temporary Resident Visa"  // 文件类别：临时居民签证
  }
}
{
  "canadian_travel_document": {                 // 加拿大旅行证信息
    "document_number": "T123456789",             // 旅行证号码
    "issued_by": "Immigration, Refugees and Citizenship Canada (IRCC)", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "15 MAR 2022",                 // 签发日期
    "expiry_date": "15 MAR 2027",                // 到期日期
    "document_type": "Canadian Travel Document", // 文件类型：加拿大旅行证
    "holder_information": {                      // 持证人信息
      "first_name": "Liam",                      // 名字
      "last_name": "Davis",                      // 姓氏
      "middle_name": "Alexander",                // 中间名（可选）
      "date_of_birth": "5 FEB 1990",             // 出生日期
      "place_of_birth": "Toronto, ON, Canada",   // 出生地点
      "sex": "Male",                             // 性别
      "nationality": "Canada",                   // 国籍：加拿大
      "address": {                               // 持证人地址
        "street": "567 Birch Rd",                // 街道地址
        "city": "Ottawa",                        // 城市
        "province": "ON",                        // 省份
        "postal_code": "K1A 0B1"                 // 邮政编码
      }
    },
    "document_category": "Travel Document",      // 文件类别：旅行证
    "travel_document_type": "Refugee Travel Document", // 旅行证类型：难民旅行证
    "security_features": [                       // 安全特征
      "Barcode",                                 // 条形码
      "Hologram",                                // 全息图
      "Magnetic Stripe"                          // 磁条
    ]
  }
}
{
  "canadian_social_insurance_number": {         // 加拿大社会保险号码信息
    "sin_number": "123-456-789",                 // 社会保险号码
    "issued_by": "Service Canada",               // 签发机构：Service Canada
    "issue_date": "10 OCT 2015",                 // 签发日期
    "holder_information": {                      // 持证人信息
      "first_name": "Emily",                     // 名字
      "last_name": "Johnson",                    // 姓氏
      "middle_name": "Rose",                     // 中间名（可选）
      "date_of_birth": "5 JAN 1992",             // 出生日期
      "place_of_birth": "Montreal, QC, Canada",  // 出生地点
      "sex": "Female",                           // 性别
      "nationality": "Canada",                   // 国籍：加拿大
      "address": {                               // 持证人地址
        "street": "456 Oak Street",              // 街道地址
        "city": "Ottawa",                        // 城市
        "province": "ON",                        // 省份
        "postal_code": "K2P 1A3"                 // 邮政编码
      }
    },
    "document_category": "Social Insurance Number", // 文件类别：社会保险号码
    "security_features": [                       // 安全特征
      "Barcode",                                 // 条形码
      "Hologram",                                // 全息图
      "Magnetic Stripe"                          // 磁条
    ]
  }
}
{
  "canadian_foreign_national_id": {             // 加拿大外国居民身份证明信息
    "id_number": "FN123456789",                  // 身份证件编号
    "issued_by": "Immigration, Refugees and Citizenship Canada (IRCC)", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "5 JUN 2020",                  // 签发日期
    "expiry_date": "5 JUN 2025",                 // 到期日期
    "document_type": "Foreign National ID",      // 文件类型：外国居民身份证明
    "holder_information": {                       // 持证人信息
      "first_name": "Ana",                        // 名字
      "last_name": "Garcia",                      // 姓氏
      "middle_name": "Maria",                     // 中间名（可选）
      "date_of_birth": "20 AUG 1994",             // 出生日期
      "place_of_birth": "Madrid, Spain",          // 出生地点
      "sex": "Female",                            // 性别
      "nationality": "Spain",                     // 国籍：西班牙
      "address": {                                // 持证人地址
        "street": "789 Pine St",                  // 街道地址
        "city": "Toronto",                        // 城市
        "province": "ON",                         // 省份
        "postal_code": "M5A 1A1"                  // 邮政编码
      }
    },
    "visa_status": "Temporary Resident",          // 签证状态：临时居民
    "document_category": "Foreign National ID",  // 文件类别：外国居民身份证明
    "security_features": [                        // 安全特征
      "Barcode",                                  // 条形码
      "Hologram",                                 // 全息图
      "Magnetic Stripe"                           // 磁条
    ]
  }
}
{
  "canadian_student_verification": {            // 加拿大学生身份证明信
    "student_number": "S123456789",               // 学生编号
    "issued_by": "University of Toronto",        // 签发机构：多伦多大学
    "issue_date": "1 SEPT 2023",                 // 签发日期
    "expiry_date": "31 AUG 2024",                // 到期日期
    "document_type": "Student Verification Letter", // 文件类型：学生身份证明信
    "holder_information": {                      // 持证人信息
      "first_name": "John",                      // 名字
      "last_name": "Doe",                        // 姓氏
      "middle_name": "Edward",                   // 中间名（可选）
      "date_of_birth": "15 MAR 2000",            // 出生日期
      "place_of_birth": "Vancouver, BC, Canada", // 出生地点
      "sex": "Male",                             // 性别
      "nationality": "Canada",                   // 国籍：加拿大
      "address": {                               // 持证人地址
        "street": "123 Maple Ave",               // 街道地址
        "city": "Toronto",                       // 城市
        "province": "ON",                        // 省份
        "postal_code": "M5T 2E7"                 // 邮政编码
      }
    },
    "program_details": {                         // 学业信息
      "program_name": "Bachelor of Computer Science", // 学位课程名称
      "start_date": "1 SEPT 2023",               // 开始日期
      "end_date": "31 AUG 2027",                 // 结束日期
      "status": "Full-time"                      // 学业状态：全日制
    },
    "document_category": "Student Verification Letter", // 文件类别：学生身份证明信
    "security_features": [                       // 安全特征
      "Watermark",                               // 水印
      "Signature of Registrar"                   // 注册处签名
    ]
  }
}
{
  "canadian_immigration_visa": {                 // 加拿大移民签证信息
    "visa_number": "IM123456789",                 // 移民签证编号
    "issued_by": "Immigration, Refugees and Citizenship Canada (IRCC)", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "15 FEB 2023",                  // 签发日期
    "expiry_date": "15 FEB 2028",                 // 到期日期
    "visa_type": "Permanent Resident Visa",       // 签证类型：永久居民签证
    "holder_information": {                       // 持证人信息
      "first_name": "Liam",                       // 名字
      "last_name": "Smith",                       // 姓氏
      "middle_name": "Alexander",                 // 中间名（可选）
      "date_of_birth": "10 NOV 1985",             // 出生日期
      "place_of_birth": "London, UK",             // 出生地点
      "sex": "Male",                              // 性别
      "nationality": "United Kingdom",            // 国籍：英国
      "address": {                                // 持证人地址
        "street": "789 Elm St",                   // 街道地址
        "city": "Toronto",                        // 城市
        "province": "ON",                         // 省份
        "postal_code": "M5H 2N2"                  // 邮政编码
      }
    },
    "immigration_program": {                      // 移民项目
      "program_name": "Express Entry",            // 移民项目名称：快速入境
      "program_type": "Federal Skilled Worker",   // 项目类型：联邦技术工人
      "application_number": "EX1234567890",       // 申请编号
      "status": "Approved"                        // 状态：已批准
    },
    "document_category": "Immigration Visa",      // 文件类别：移民签证
    "security_features": [                        // 安全特征
      "Barcode",                                  // 条形码
      "Hologram",                                 // 全息图
      "Magnetic Stripe"                           // 磁条
    ]
  }
}
{
  "canadian_permanent_resident_card": {          // 加拿大永久居民卡信息
    "card_number": "PR1234567890",                // 永久居民卡号码
    "issued_by": "Immigration, Refugees and Citizenship Canada (IRCC)", // 签发机构：加拿大移民、难民和公民事务部（IRCC）
    "issue_date": "15 JAN 2023",                  // 签发日期
    "expiry_date": "15 JAN 2028",                 // 到期日期
    "document_type": "Permanent Resident Card",   // 文件类型：永久居民卡
    "holder_information": {                       // 持证人信息
      "first_name": "Olivia",                     // 名字
      "last_name": "Johnson",                     // 姓氏
      "middle_name": "Grace",                     // 中间名（可选）
      "date_of_birth": "5 JUN 1990",              // 出生日期
      "place_of_birth": "Montreal, QC, Canada",   // 出生地点
      "sex": "Female",                            // 性别
      "nationality": "Canada",                    // 国籍：加拿大
      "address": {                                // 持证人地址
        "street": "101 Maple St",                 // 街道地址
        "city": "Toronto",                        // 城市
        "province": "ON",                         // 省份
        "postal_code": "M5A 1A1"                  // 邮政编码
      }
    },
    "immigration_status": "Permanent Resident",   // 移民状态：永久居民
    "document_category": "Permanent Resident Card", // 文件类别：永久居民卡
    "security_features": [                        // 安全特征
      "Barcode",                                  // 条形码
      "Hologram",                                 // 全息图
      "Microchip"                                 // 微芯片
    ]
  }
}
{
  "birth_certificate": {                       // 出生证明
    "name": "John Doe",                        // 新生儿姓名
    "date_of_birth": "01 JAN 2023",            // 出生日期
    "place_of_birth": {                        // 出生地点
      "city": "New York",                      // 出生城市
      "state": "New York",                     // 出生州
      "hospital": "ABC Hospital"               // 出生医院（可选）
    },
    "gender": "Male",                          // 性别
    "birth_order": "First",                    // 出生顺序
    "parents": {                               // 父母信息
      "father": {                              // 父亲信息
        "name": "James Doe",                   // 父亲姓名
        "date_of_birth": "15 JUN 1980",         // 父亲出生日期（可选）
        "place_of_birth": "Los Angeles, CA"     // 父亲出生地点（可选）
      },
      "mother": {                               // 母亲信息
        "name": "Mary Doe",                    // 母亲姓名
        "date_of_birth": "10 MAY 1985",         // 母亲出生日期（可选）
        "place_of_birth": "Chicago, IL",        // 母亲出生地点（可选）
        "marital_status": "Married",            // 婚姻状况
        "address": "123 Main St, New York, NY"  // 母亲住址
      }
    },
    "attending_physician": {                    // 接生医生信息
      "name": "Dr. Emily Smith",               // 医生姓名
      "license_number": "1234567"               // 医生执业号码（可选）
    },
    "certificate_number": "123456789",         // 证书号码
    "issue_date": "10 FEB 2023",               // 证书签发日期
    "registration_info": {                     // 登记信息
      "registration_number": "987654321",      // 注册号
      "registered_at": "New York County Health Department" // 注册机构
    },
    "official_seal_and_signature": {           // 官方签名和印章
      "signature": "John Registration",        // 签发人签名
      "seal": "Official Seal of the State of New York" // 官方印章
    }
  }
}
{
  "non_immigrant_visa": {                           // 非移民签证信息
    "visa_type": "B-1/B-2",                         // 签证类型：B-1/B-2（商务/旅游签证）
    "visa_number": "123456789",                      // 签证编号
    "passport_number": "C03005988",                  // 护照编号
    "issued_by": "U.S. Department of State",         // 签发机构：美国国务院
    "issue_date": "15 JUN 2023",                     // 签发日期
    "expiry_date": "15 JUN 2028",                    // 到期日期
    "applicant": {                                   // 申请人信息
      "first_name": "John",                          // 名字
      "last_name": "Doe",                            // 姓氏
      "date_of_birth": "01 JAN 1990",                // 出生日期
      "gender": "Male",                              // 性别
      "nationality": "USA",                          // 国籍
      "place_of_birth": "Los Angeles, CA",           // 出生地
      "passport_country": "USA",                     // 护照签发国
      "address": "123 Main St, New York, NY"         // 申请人住址
    },
    "visa_status": "Approved",                       // 签证状态：已批准
    "purpose_of_travel": "Business and Tourism",     // 旅行目的：商务和旅游
    "application_number": "987654321",               // 申请号
    "interview_location": "U.S. Embassy, New York",  // 面试地点：美国大使馆，纽约
    "supporting_documents": [                        // 支持性文件
      {
        "document_type": "I-20",                     // 支持文件类型：I-20（学生签证表格）
        "document_number": "567890123"               // 文件编号
      },
      {
        "document_type": "Invitation Letter",        // 支持文件类型：邀请函
        "document_number": "987654321"               // 文件编号
      }
    ],
    "security_features": ["Barcode", "Passport Photo"], // 安全特征：条形码、护照照片
    "visa_category": "Tourist and Business",           // 签证类别：旅游和商务
    "document_category": "Nonimmigrant Visa"          // 文件类别：非移民签证
  }
}
{
  "international_travel_document": {              // 国际旅行证件
    "document_type": "Passport",                   // 证件类型：护照
    "passport_number": "C03005988",                // 护照编号
    "passport_card_number": "C03005988",           // 护照卡编号（如果适用）
    "issued_by": "U.S. Department of State",       // 签发机构：美国国务院
    "issue_date": "30 NOV 2009",                   // 签发日期
    "expiry_date": "29 NOV 2019",                  // 到期日期
    "document_status": "EXEMPLAR",                 // 证件状态：示例（EXEMPLAR）
    "nationality": "USA",                          // 国籍：美国
    "surname": "TRAVELER",                         // 姓氏
    "given_names": "HAPPY",                        // 名字
    "sex": "M",                                    // 性别
    "date_of_birth": "1 JAN 1981",                 // 出生日期
    "place_of_birth": "New York, U.S.A.",          // 出生地点
    "place_of_issue": "Washington, D.C.",          // 签发地点
    "barcode_and_security_features": "Included",   // 条形码和安全特征：已包含
    "passport_photo": "Included",                  // 护照照片：已包含
    "travel_document_purpose": "Identification",   // 旅行证件用途：身份识别
    "document_category": "Travel Document"        // 文件类别：旅行文件
  }
}
{
  "taxpayer_identification_number": {          // 纳税人识别号信息
    "tin_type": "SSN",                          // TIN类型：社会安全号码（SSN）
    "tin_number": "123-45-6789",                 // 纳税人识别号
    "issued_by": "Social Security Administration", // 签发机构：社会安全局（SSA）
    "issue_date": "01 JAN 2000",                 // 签发日期
    "taxpayer_name": {                           // 纳税人信息
      "first_name": "John",                      // 名字
      "last_name": "Doe",                        // 姓氏
      "middle_name": "A",                        // 中间名（可选）
      "date_of_birth": "15 JUN 1980",            // 出生日期
      "place_of_birth": "Los Angeles, CA",       // 出生地点
      "nationality": "USA"                       // 国籍
    },
    "address": {                                 // 纳税人地址
      "street": "456 Oak St",                    // 街道地址
      "city": "Los Angeles",                     // 城市
      "state": "CA",                             // 州
      "zip_code": "90001"                        // 邮政编码
    },
    "taxpayer_status": "Active",                 // 纳税人状态：有效
    "tax_category": "Individual",                // 税务类别：个人
    "social_security_status": "Issued",          // 社会安全号状态：已签发
    "ein_number": null                           // 如果有EIN则填写，如果无则为null
  }
}
{
  "passport_card": {
    "type": "passport_card", // 类型：护照卡
    "passport_type": "P", // 护照类型：P（普通护照）
    "country_code": "USA", // 国家代码：美国
    "passport_number": "C03005988", // 护照编号
    "surname": "TRAVELER", // 姓氏：旅行者
    "given_names": "HAPPY", // 名字：快乐
    "nationality": "USA", // 国籍：美国
    "date_of_birth": "1 JAN 1981", // 出生日期：1981年1月1日
    "place_of_birth": "NEW YORK, U.S.A.", // 出生地：美国纽约
    "sex": "M", // 性别：男性
    "date_of_issue": "30 NOV 2009", // 护照签发日：2009年11月30日
    "issuing_authority": "UNITED STATES DEPARTMENT OF STATE", // 签发机构：美国国务院
    "expiration_date": "29 NOV 2019", // 有效日期：2019年11月29日
    "endorsements": "None", // 背书：无（此处为占位，若有背书信息可以填充）
  }
}
{
  "drivers_license": {                           // 驾驶执照信息
    "license_number": "D123456789",               // 驾驶执照编号
    "state_of_issue": "California",               // 签发州：加利福尼亚州
    "issued_by": "California Department of Motor Vehicles", // 签发机构：加州机动车管理局
    "issue_date": "15 JUN 2015",                  // 签发日期
    "expiry_date": "15 JUN 2025",                 // 到期日期
    "license_type": "Class C",                    // 执照类型：C类（普通驾照）
    "license_status": "Valid",                    // 执照状态：有效
    "driver_information": {                       // 驾驶员信息
      "first_name": "John",                       // 名字
      "last_name": "Doe",                         // 姓氏
      "middle_name": "A",                         // 中间名（可选）
      "date_of_birth": "15 JUN 1980",             // 出生日期
      "place_of_birth": "Los Angeles, CA",        // 出生地点
      "nationality": "USA",                       // 国籍
      "sex": "Male",                              // 性别
      "height": "6'0\"",                          // 身高
      "eye_color": "Brown",                       // 眼睛颜色
      "hair_color": "Black"                       // 头发颜色
    },
    "address": {                                  // 驾驶员地址
      "street": "123 Main St",                    // 街道地址
      "city": "Los Angeles",                      // 城市
      "state": "CA",                              // 州
      "zip_code": "90001"                         // 邮政编码
    },
    "photo_included": "Yes",                      // 是否包含照片：是
    "security_features": [                        // 安全特征
      "Hologram",                                 // 全息图
      "Barcode",                                  // 条形码
      "Magnetic Stripe"                           // 磁条
    ],
    "document_category": "Driver's License"       // 文件类别：驾驶执照
  }
}
{
  "military_id": {                              // 美国军事身份证信息
    "id_number": "123456789",                    // 身份证编号
    "issued_by": "Department of Defense",        // 签发机构：美国国防部
    "issue_date": "01 JAN 2020",                 // 签发日期
    "expiry_date": "01 JAN 2025",                // 到期日期
    "military_branch": "Army",                   // 军种：美国陆军
    "id_type": "Active Duty",                    // 身份证类型：现役军人
    "military_rank": "Sergeant",                 // 军衔：军士
    "military_status": "Active",                 // 军事状态：现役
    "service_number": "9876543210",              // 服务编号
    "dependent": false,                          // 是否为军属：否
    "photo_included": "Yes",                     // 是否包含照片：是
    "security_features": [                       // 安全特征
      "Hologram",                                // 全息图
      "Barcode",                                 // 条形码
      "Magnetic Stripe"                          // 磁条
    ],
    "military_member": {                         // 军人个人信息
      "first_name": "John",                      // 名字
      "last_name": "Doe",                        // 姓氏
      "middle_name": "A",                        // 中间名（可选）
      "date_of_birth": "15 MAR 1990",            // 出生日期
      "place_of_birth": "Los Angeles, CA",       // 出生地点
      "sex": "Male",                             // 性别
      "nationality": "USA",                      // 国籍
      "height": "6'2\"",                         // 身高
      "eye_color": "Green",                      // 眼睛颜色
      "hair_color": "Brown"                      // 头发颜色
    },
    "address": {                                 // 地址
      "street": "123 Army St",                   // 街道地址
      "city": "Washington",                      // 城市
      "state": "DC",                             // 州
      "zip_code": "20001"                        // 邮政编码
    },
    "document_category": "Military ID"           // 文件类别：军事身份证
  }
}
{
  "un_international_organization_card": {      // 联合国国际组织卡信息
    "id_number": "UN123456789",                 // 卡片编号
    "issued_by": "United Nations",              // 签发机构：联合国
    "issue_date": "01 JAN 2018",                // 签发日期
    "expiry_date": "01 JAN 2023",               // 到期日期
    "card_type": "Staff ID",                    // 卡片类型：工作人员身份证明
    "organization": "United Nations",           // 所属组织：联合国
    "position": "Senior Advisor",               // 职位：高级顾问
    "status": "Active",                         // 身份状态：有效
    "photo_included": "Yes",                    // 是否包含照片：是
    "security_features": [                      // 安全特征
      "Hologram",                               // 全息图
      "Barcode",                                // 条形码
      "QR Code"                                 // 二维码
    ],
    "holder_information": {                     // 持卡人信息
      "first_name": "Jane",                     // 名字
      "last_name": "Smith",                     // 姓氏
      "middle_name": "A",                       // 中间名（可选）
      "date_of_birth": "25 DEC 1985",           // 出生日期
      "place_of_birth": "New York, USA",        // 出生地点
      "sex": "Female",                          // 性别
      "nationality": "USA",                     // 国籍
      "height": "5'6\"",                        // 身高
      "eye_color": "Blue",                      // 眼睛颜色
      "hair_color": "Blonde"                    // 头发颜色
    },
    "address": {                                // 持卡人地址
      "street": "456 UN Plaza",                 // 街道地址
      "city": "New York",                       // 城市
      "state": "NY",                            // 州
      "zip_code": "10017"                       // 邮政编码
    },
    "document_category": "UN International Organization Card" // 文件类别：联合国国际组织卡
  }
}
{
  temporary_work_card {                       临时工作卡信息
    card_number W123456789,                  卡片编号
    issued_by USCIS,                         签发机构：美国公民及移民服务局（USCIS）
    issue_date 01 JUN 2020,                  签发日期
    expiry_date 01 JUN 2022,                 到期日期
    work_permission_type Temporary,          工作许可类型：临时工作许可
    status Active,                           状态：有效
    work_restrictions Employment Only with Authorized Employer,  工作限制：仅限于授权雇主的工作
    photo_included Yes,                      是否包含照片：是
    security_features [                        安全特征
      Hologram,                                 全息图
      Barcode,                                  条形码
      Magnetic Stripe                           磁条
    ],
    holder_information {                       持卡人信息
      first_name Alice,                      名字
      last_name Johnson,                     姓氏
      middle_name B,                         中间名（可选）
      date_of_birth 15 JUL 1995,             出生日期
      place_of_birth Chicago, IL,            出生地点
      sex Female,                            性别
      nationality USA,                       国籍
      visa_status H-1B,                      签证状态：H-1B签证
      expiration_of_visa 01 JUN 2023         签证到期日期
    },
    address {                                  持卡人地址
      street 789 Work Ave,                   街道地址
      city Chicago,                          城市
      state IL,                              州
      zip_code 60601                         邮政编码
    },
    document_category Temporary Work Card    文件类别：临时工作卡
  }
}
{
  "green_card": {                               // 美国绿卡信息
    "card_number": "A123456789",                 // 绿卡号码
    "issued_by": "USCIS",                        // 签发机构：美国公民及移民服务局（USCIS）
    "issue_date": "01 JAN 2018",                 // 签发日期
    "expiry_date": "01 JAN 2028",                // 到期日期
    "resident_type": "Permanent Resident",       // 居民类型：永久居民
    "status": "Active",                          // 状态：有效
    "photo_included": "Yes",                     // 是否包含照片：是
    "security_features": [                       // 安全特征
      "Hologram",                                // 全息图
      "Barcode",                                 // 条形码
      "Magnetic Stripe"                          // 磁条
    ],
    "holder_information": {                      // 持卡人信息
      "first_name": "John",                      // 名字
      "last_name": "Doe",                        // 姓氏
      "middle_name": "A",                        // 中间名（可选）
      "date_of_birth": "15 MAR 1980",            // 出生日期
      "place_of_birth": "New York, NY",          // 出生地点
      "sex": "Male",                             // 性别
      "nationality": "USA",                      // 国籍
      "alien_number": "A123456789",              // 外籍人员编号
      "height": "5'11\"",                        // 身高
      "eye_color": "Brown",                      // 眼睛颜色
      "hair_color": "Black"                      // 头发颜色
    },
    "address": {                                 // 持卡人地址
      "street": "123 Main St",                   // 街道地址
      "city": "Los Angeles",                     // 城市
      "state": "CA",                             // 州
      "zip_code": "90001"                        // 邮政编码
    },
    "document_category": "Permanent Resident Card"  // 文件类别：永久居民卡
  }
}
{
  "social_security_card": {                    // 美国社会保障卡信息
    "ssn_number": "123-45-6789",                // 社会保障号码（SSN）
    "issued_by": "Social Security Administration", // 签发机构：美国社会保障局（SSA）
    "issue_date": "01 JAN 2000",                // 签发日期
    "card_type": "Standard",                    // 卡片类型：标准卡
    "status": "Active",                          // 状态：有效
    "holder_information": {                      // 持卡人信息
      "first_name": "John",                      // 名字
      "last_name": "Doe",                        // 姓氏
      "middle_name": "A",                        // 中间名（可选）
      "date_of_birth": "15 MAR 1985",            // 出生日期
      "place_of_birth": "Los Angeles, CA",       // 出生地点
      "sex": "Male",                             // 性别
      "nationality": "USA",                      // 国籍
      "address": {                               // 持卡人地址
        "street": "123 Main St",                 // 街道地址
        "city": "Los Angeles",                   // 城市
        "state": "CA",                           // 州
        "zip_code": "90001"                      // 邮政编码
      }
    },
    "security_features": [                       // 安全特征
      "Hologram",                                // 全息图
      "Barcode",                                 // 条形码
      "Magnetic Stripe"                          // 磁条
    ],
    "document_category": "Social Security Card"  // 文件类别：社会保障卡
  }
}
{
  "permanent_resident_card": {                    // 美国永久居民卡信息
    "card_number": "A123456789",                   // 绿卡号码
    "issued_by": "USCIS",                          // 签发机构：美国公民及移民服务局（USCIS）
    "issue_date": "01 JAN 2018",                   // 签发日期
    "expiry_date": "01 JAN 2028",                  // 到期日期
    "resident_type": "Permanent Resident",         // 居民类型：永久居民
    "status": "Active",                            // 状态：有效
    "photo_included": "Yes",                       // 是否包含照片：是
    "security_features": [                         // 安全特征
      "Hologram",                                  // 全息图
      "Barcode",                                   // 条形码
      "Magnetic Stripe"                            // 磁条
    ],
    "holder_information": {                        // 持卡人信息
      "first_name": "John",                        // 名字
      "last_name": "Doe",                          // 姓氏
      "middle_name": "A",                          // 中间名（可选）
      "date_of_birth": "15 MAR 1980",              // 出生日期
      "place_of_birth": "New York, NY",            // 出生地点
      "sex": "Male",                               // 性别
      "nationality": "USA",                        // 国籍
      "alien_number": "A123456789",                // 外籍人员编号
      "height": "5'11\"",                          // 身高
      "eye_color": "Brown",                        // 眼睛颜色
      "hair_color": "Black"                        // 头发颜色
    },
    "address": {                                   // 持卡人地址
      "street": "1234 Maple St",                   // 街道地址
      "city": "Los Angeles",                       // 城市
      "state": "CA",                               // 州
      "zip_code": "90001"                          // 邮政编码
    },
    "document_category": "Permanent Resident Card" // 文件类别：永久居民卡
  }
}
招商银行信用卡对账单（个人消费卡账户 2024年12月）（补）
CMB Credit Card Statement (2024.12)

430200

湖北省武汉市

江夏区光谷汇金中心１１Ｈ栋３层北京阿博茨科技有限

公司

张帅

账单日
账单日  
2024年12月05日
Statement Date  
信用额度  
¥ 10,000.00
Credit Limit  
到期还款日  
2024年12月23日
Payment Due Date  
本期还款总额  
¥ 7,667.73
¥ 383.39
Current Balance  
本期最低还款额  
Minimum Payment
 11/13 11/14 giffgaff 93.56 3131 10.00(GB)
 11/14 11/16 ULTRA MOBILE 36.28 3131 5.00(US)
 11/14 11/16 ULTRA MOBILE 39.40 3131 5.43(US)
 11/14 11/16 ULTRA MOBILE 78.80 3131 10.86(US)
 11/18 11/19 ULTRA MOBILE 39.38 3131 5.43(US)
 11/18 11/19 ULTRA MOBILE 39.38 3131 5.43(US)
 11/18 11/20 ULTRA MOBILE 39.41 3131 5.43(US)
 11/18 11/20 ULTRA MOBILE 78.83 3131 10.86(US)
 11/18 11/20 ULTRA MOBILE 23.66 3131 3.26(US)
 11/19 11/21 ULTRA MOBILE 39.44 3131 5.43(US)
 11/20 11/21 ULTRA MOBILE 39.44 3131 5.43(US)
 11/27 11/29 Telegram Premium 209.99 3131 209.99(GB)
 11/28 11/29 财付通-达美乐比萨 53.50 9615 53.50(CN)
 11/30 12/01 财付通-沃尔玛 103.43 9615 103.43(CN)
 11/30 12/01 财付通-沃尔玛 63.57 9615 63.57(CN)
 12/01 12/02 财付通-达美乐比萨 32.50 9615 32.50(CN)
 12/03 12/04 财付通-牛泰吉（千宝店） 18.00 9615 18.00(CN)
 】  
本期还款总额
Current Balance =
上期账单金额
Balance B/F -
上期还款金额
Payment +
本期账单金额
New Charges -
本期调整金额
Adjustment +
循环利息
Interest
¥ 7,667.73 ¥ 0.00 ¥ 0.00 ¥ 7,667.73 ¥ 0.00 ¥ 0.00
(1)上述交易摘要中的商户名称仅供您参考，如与签购单不符，请以签购单为准。  
(2)若您的人民币或美元账户的'本期应还金额'为负数，表示本期该人民币或美元账户中尚有存款，您不需另行还款，本期账单仅供您作为对账参考。  
(3)通过本行系统缴款，您的信用额度一般可于缴款后立即恢复。  
★友情提醒：依据《征信业管理条例》相关规定，我行会如实上报您的个人信用信息至金融信用信息基础数据库，该信息将对您与银行等
金融机构发生的借贷业务产生重要影响，为维护良好的信用记录，请您及时还款！

个人消费卡账户 2025年01月
SOLD POSTED DESCRIPTION RMB AMOUNT CARD NO(Last 4digits) Original Tran Amount
还款
 12/12 掌上生活还款回馈金 -1.00 3131 -1.00
 12/12 掌上生活还款 -7,666.73 3131 -7,666.73
费用
 12/25 12/25 挂失费 60.00 9615 60.00
 12/30 12/30 挂失费 60.00 3131 60.00
 12/30 12/31 挂失费调减 -60.00 3131 -60.00
退款
 12/19 12/20 财付通-腾讯云费用账户-移动支付 -100.00 9615 -100.00(CN)
消费
 12/05 12/07 X CORP. PAID FEATURES 59.12 3131 63.00(US)
 12/10 12/12 ULTRA MOBILE 36.41 3131 5.00(US)
 12/12 12/14 Amazon web services 6,642.40 3131 909.98(US)
 12/16 12/17 财付通-滴滴出行 13.67 9615 13.67(CN)
 12/16 12/17 财付通-牛泰吉（千宝店） 8.00 9615 8.00(CN)
 12/17 12/18 财付通-武汉光谷现代有轨电车运营有限 2.00 9615 2.00(CN)
 12/17 12/18 财付通-牛泰吉（千宝店） 10.00 9615 10.00(CN)
 12/19 12/20 财付通-牛泰吉（千宝店） 8.00 9615 8.00(CN)
 12/19 12/20 财付通-腾讯云费用账户-移动支付 100.00 9615 100.00(CN)
 12/20 12/21 财付通-滴滴出行 17.25 9615 17.25(CN)
 还款
 01/08 掌上生活还款 -3,992.00 2138 -3,992.00
 01/08 掌上生活还款回馈金 -8.00 2138 -8.00
 01/09 掌上生活还款 -74.00 2138 -74.00
 01/23 掌上生活还款 -2,918.10 2138 -2,918.10
消费
 01/08 01/09 ULTRA MOBILE 23.97 2138 3.26(US)
 01/09 01/10 ULTRA MOBILE 39.93 2138 5.43(US)
 01/09 01/11 Amazon web services 6,851.04 2138 931.05(US)
 01/09 01/11 ULTRA MOBILE 39.96 2138 5.43(US)
 01/21 01/23 DNH*GODADDY.COM HKD 76.86 2138 81.90(NL)
本期还款总额
Current Balance =
上期账单金额
Balance B/F -
上期还款金额
Payment +
本期账单金额
New Charges -
本期调整金额
Adjustment +
循环利息
Interest
¥ 7,031.76 ¥ 6,992.10 ¥ 6,992.10 ¥ 7,031.76 ¥ 0.00 ¥ 0.00
(1)上述交易摘要中的商户名称仅供您参考，如与签购单不符，请以签购单为准。  
还款
 02/10 掌上生活还款 -7,023.76 2138 -7,023.76
 02/10 掌上生活还款回馈金 -8.00 2138 -8.00
消费
 02/07 02/08 ULTRA MOBILE 39.77 2138 5.43(US)
 02/08 02/09 ULTRA MOBILE 73.23 2138 10.00(US)
 02/08 02/09 ULTRA MOBILE 81.14 2138 11.08(US)
 02/08 02/09 ULTRA MOBILE 81.14 2138 11.08(US)
 02/08 02/10 ULTRA MOBILE 39.78 2138 5.43(US)
 02/13 02/15 Amazon web services 6,771.59 2138 929.18(US)
 02/17 02/19 giffgaff 92.24 2138 10.00(GB)
 02/24 02/26 giffgaff 92.23 2138 10.00(GB)
 02/24 02/26 giffgaff 92.23 2138 10.00(GB)
 02/24 02/26 giffgaff 92.23 2138 10.00(GB)
 02/26 02/28 ULTRA MOBILE 73.10 2138 10.00(US)
 02/26 02/28 ULTRA MOBILE 73.10 2138 10.00(US)
 02/26 02/28 ULTRA MOBILE 77.64 2138 10.62(US)
"""


def get_refer(question: str) -> str:
    llm = ai_engine.get_openai_model()
    return llm.invoke(f"{all_file}\n\n 从以上信息中提取与问题”{question}“相关的数据给我，不需要分析，把原文整理给我就行，除了原文不要回答我别的文字")