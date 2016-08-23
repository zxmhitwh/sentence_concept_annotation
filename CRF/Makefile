
VERSION = 1.0.0.2
WORKROOT = ./utlis_lib
PUBLIC = $(WORKROOT)/public
NLP = $(WORKROOT)
LIB2 = $(WORKROOT)/lib2-64
LIBNAME = crfpp
THIRD = $(WORKROOT)/third-64

SRC_DIR = src
BIN_DIR = bin
INCLUDE_DIR = include
OUTPUT_DIR = output
LIB_DIR = lib
TEST_DIR = test

SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst %.cpp,%.o,$(SOURCES))

TEST_SOURCES = $(wildcard $(TEST_DIR)/*.cpp)
TEST_BINS = $(patsubst %.cpp,%,$(TEST_SOURCES))

#-----------------------------------------------------------------------#
INCLUDEFLAGS = -I./$(INCLUDE_DIR) \
	       -I $(WORKROOT)/nlpseg/include \
			-I../pinyin_zhuyin/output/include/\
			-I$(NLP)/hci/parsing/dep-parser/include \
			-I$(LIB2)/ml/linear-models/include \
			-I$(LIB2)/ml/commonlib/include \
			-I$(NLP)/hci/crf-postag/include \
			-I$(LIB2)/wordseg \
			-I$(LIB2)/libcrf/include \
			-I$(LIB2)/others-ex/include \
			-I$(LIB2)/bsl/include \
			-I$(LIB2)/ml/hmm/include \
			-I$(PUBLIC)/odict \
			-I$(PUBLIC)/sign/output/include \
			-I$(LIB2)/dict/include \
			-I$(LIB2)/ullib/include \
			-I$(LIB2)/ccode/include \
			-I$(THIRD)/pcre/include\
	       -I../triedict/output/include/\

LIBFLAGS =	-L./$(LIB_DIR)/ \
			-lpthread\
			-lm

CXXFLAGS = -g -Wall -fpermissive -W -pipe -fPIC
CXX = g++ $(CXXFLAGS)

.PHONY: all test lib release clean

#-----------------------------------------------------------------------#
# make all                                                              #
#-----------------------------------------------------------------------#
all : lib test output

#-----------------------------------------------------------------------#
# make lib                                                              #
#-----------------------------------------------------------------------#
lib : $(OBJS)
	if [ ! -d $(LIB_DIR) ]; then mkdir $(LIB_DIR); fi
	ar -ruv $(LIB_DIR)/lib$(LIBNAME).a $(OBJS)

$(OBJS): %.o: %.cpp
	$(CXX) -c $< -o $@ $(INCLUDEFLAGS)

output : 
	if [ ! -d $(OUTPUT_DIR) ]; then mkdir $(OUTPUT_DIR); fi
	cp -r $(INCLUDE_DIR) $(OUTPUT_DIR)
	cp -r $(LIB_DIR) $(OUTPUT_DIR)
	cp -r $(BIN_DIR) $(OUTPUT_DIR)

#-----------------------------------------------------------------------#
# make test                                                             #
#-----------------------------------------------------------------------#
test: $(TEST_BINS)

$(TEST_BINS): %: %.cpp
	if [ ! -d $(BIN_DIR) ]; then mkdir $(BIN_DIR); fi
	$(CXX) $< -o $@ $(INCLUDEFLAGS) -l$(LIBNAME) $(LIBFLAGS)
	mv $@ $(BIN_DIR)/

clean :
	rm -rf $(LIB_DIR)/lib$(LIBNAME).a
	rm -rf $(OBJS)
	rm -rf $(SRC_DIR)/*.o $(SRC_DIR)/*~
	rm -f $(BIN_DIR)/*
